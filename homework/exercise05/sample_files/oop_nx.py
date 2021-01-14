import os

from typing import Optional
from collections import Counter

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


DNA = 'dna'
RNA = 'rna'
PROTEIN = 'protein'
MOLECULE = 'molecule'
SYMBOL = 'symbol'


class Network:
    """Represents a general biological network."""

    def __init__(self, node_list: str = None, edge_list: str = None, ppi_file: str = None, enrich: bool = False):
        self.nodes = None
        self.graph = None
        self._ppi_path = ppi_file
        self.enrich = enrich
        self.__reverse_mapper = None  # Used for creating a reverse lookup

        if ppi_file and (node_list and edge_list):
            raise ImportError("Please load either a PPI file OR a node list and edge list, not all 3!")

        if node_list and edge_list:
            self.import_nodes(node_list)  # Assigns nodes to self.nodes
            self.import_graph(edge_list)  # Assigns graph to self.graph

        if ppi_file:
            self.import_ppi()  # Assigns nodes to self.nodes AND graph to self.graph

        if self.enrich:
            self.enrich_graph()

    def enrich_graph(self):
        """Wrapper method for adding RNA/DNA nodes and associated edges."""
        self.__reverse_map_nodes()
        self.__enrich_nodes()
        self.__enrich_edges()

    def __reverse_map_nodes(self) -> None:
        """Reverses the node lookup dict so symbol is the key."""
        self.__reverse_mapper = dict()
        for node_id, metadata in self.nodes.items():
            if metadata[SYMBOL] not in self.__reverse_mapper:
                self.__reverse_mapper[metadata[SYMBOL]] = {metadata[MOLECULE]: node_id}
            else:
                self.__reverse_mapper[metadata[SYMBOL]][metadata[MOLECULE]] = node_id

    def __enrich_nodes(self) -> None:
        """Adds DNA and RNA nodes to self.nodes"""
        index = len(self.nodes)
        for symbol, metadata in self.__reverse_mapper.items():
            molecules = metadata.keys()
            for enriched_molecule in [RNA, DNA]:
                if enriched_molecule not in molecules:
                    index += 1
                    self.nodes[index] = {SYMBOL: symbol, MOLECULE: enriched_molecule}
                    self.__reverse_mapper[symbol][enriched_molecule] = index

    def __enrich_edges(self) -> None:
        """Adds transcribed and translated edges to graph."""
        for symbol, metadata in self.__reverse_mapper.items():
            trxn_edge = (metadata[DNA], metadata[RNA])
            trnl_edge = (metadata[RNA], metadata[PROTEIN])
            self.graph.add_edge(*trxn_edge, rel_type='transcribed')
            self.graph.add_edge(*trnl_edge, rel_type='translated')

    def __read_ppis(self) -> list:
        """Reads a file of PPIs.

        Returns
        -------
        list
            List of individual relationships found in PPI file.
        """
        if self._ppi_path is not None:
            with open(self._ppi_path, 'r') as ppif:
                content = ppif.readlines()
            # Create list of relation tuples
            return [tuple(x.strip().split(",")) for x in content[1:]]

        else:
            raise ValueError("No PPI file loaded!")

    def import_ppi(self) -> None:
        """Generates a dictionary mapping unique integer identifiers to HGNC symbols extracted from PPI
        relationship list and compiles relations into a nx.Graph.
        """
        nodes = set()
        relations = self.__read_ppis()
        for rel in relations:
            nodes.add(rel[0])
            nodes.add(rel[2])
        # Make a dictionary relating symbol to identifier
        node_mapper = {symbol: index + 1 for index, symbol in enumerate(nodes)}
        self.nodes = {node_id: {SYMBOL: symbol, MOLECULE: PROTEIN} for symbol, node_id in node_mapper.items()}

        edge_list = [f"{node_mapper[rel[0]]} {node_mapper[rel[2]]} {rel[1].replace(' ', '_')}" for rel in relations]
        self.graph = nx.parse_edgelist(edge_list, delimiter=" ", nodetype=int, data=(('rel_type', str),))

    def import_graph(self, edge_file_path: str):
        """Generate a NetworkX graph from an edge list file.

        Parameters
        ----------
        edge_file_path : str
            File path for edge list.
        """
        self.graph = nx.read_edgelist(edge_file_path, delimiter='\t',nodetype=int, data=(('rel_type', str),))

    def import_nodes(self, node_file_path: str) -> None:
        """Reads the nodes identifier/HGNC symbol from a node list file.

        Parameters
        ----------
        node_file_path : str
            File path for node list.
        """
        with open(node_file_path, 'r') as node_f:
            content = node_f.readlines()
        self.nodes = dict()
        for line in content:
            components = line.strip().split("\t")
            if len(components) == 2:  # Not enriched
                self.nodes[int(components[0])] = {SYMBOL: components[1], MOLECULE: PROTEIN}
            elif len(components) == 3:  # Enriched
                self.nodes[int(components[0])] = {SYMBOL: components[1], MOLECULE: components[2]}
            else:
                raise ImportError(f"The following line in the nodes file is not formatted correctly:\n{line}")

    def __write_node_list(self, node_file_path: str) -> None:
        """Writes unique nodes to a tab separated file with identifier in first column and HGNC symbol in second.

        Parameters
        ----------
        node_file_path : str
            File path for node list.
        """
        with open(node_file_path, 'w') as node_f:
            for node_id, metadata in self.nodes.items():
                components = [str(node_id), metadata[SYMBOL], metadata[MOLECULE]]
                node_f.write('\t'.join(components) + '\n')

    def __write_edge_list(self, edge_file_path: str) -> None:
        """Writes the edge relations to a tab separated file.

        Parameters
        ----------
        edge_file_path : str
            File path for edge list.
        """
        nx.write_edgelist(self.graph, edge_file_path, delimiter="\t", data=['rel_type'])

    def compile_files(self, node_file_path: str, edge_file_path: str) -> None:
        """Wrapper function for generating node/edge lists from a PPI file. Generates a node list and an edge at the
        given paths.

        Parameters
        ----------
        node_file_path : str
            File path location to write the node list to.
        edge_file_path : str
            File path location to write the node list to.
        """
        self.__write_node_list(node_file_path)
        self.__write_edge_list(edge_file_path)


class Analyzer(Network):
    """Analyzes the graph to find shortest paths and produce images"""

    def __init__(self, node_list: str = None, edge_list: str = None, ppi_file: str = None, enrich: bool = False):
        super().__init__(node_list, edge_list, ppi_file, enrich)
        self.paths = None

    @staticmethod
    def __check_output(graph_output_path: str) -> None:
        """Checks if the output path extension is valid.

        Parameters
        ----------
        graph_output_path : str
            Path to output the generated graph image.

        Raises
        ------
        ValueError
            If graph_output_path extension not in ("pdf", "svg", "png", "jpg")
        """
        accepted_extensions = ("pdf", "svg", "png", "jpg")
        base_name = os.path.basename(graph_output_path)
        output_extension = base_name.split(".")[1]
        if output_extension not in accepted_extensions:
            raise ValueError('Graph image must be either "pdf", "svg", "png", or "jpg"!')

    def __color_nodes(self) -> dict:
        """Creates an dict of node_id to node color: Red for proteins, Blue for RNA, and Green for DNA.

        Returns
        -------
        dict
            Returns a mapping dict with node IDs as keys and color based on molecule type as value.
        """
        color_mapper = {PROTEIN: 'red', RNA: 'blue', DNA: 'green'}
        return {node_id: color_mapper[metadata[MOLECULE]] for node_id, metadata in self.nodes.items()}

    def generate_graph_image(self, graph_output_path: str, with_edge_labels: bool = False) -> None:
        """Creates an image of a network compiled from NetworkX graph and node dictionary.

        Parameters
        ----------
        graph_output_path : str
            Path to output the generated graph image.
        with_edge_labels : bool
            Adds relation type as edge labels to image if True. Default False
        """
        self.__check_output(graph_output_path)  # Do first so you don't waste time
        node_colors = self.__color_nodes()

        if self.paths is not None:
            node_colors, edge_colors = self.__color_paths(original_node_colors=node_colors)
        else:
            node_colors, edge_colors = node_colors.values(), 'black'

        plt.figure(figsize=(18, 18))  # initialize figure with size
        node_labels = {node_id: metadata[SYMBOL] for node_id, metadata in self.nodes.items()}
        graph_pos = nx.spring_layout(self.graph, k=0.1)
        nx.draw_networkx(self.graph, pos=graph_pos,
                         with_labels=True,
                         labels=node_labels,
                         font_size=5,
                         node_color=node_colors,
                         edge_color=edge_colors,
                         alpha=0.3,
                         node_size=30,)
        if with_edge_labels:
            edge_labels = nx.get_edge_attributes(self.graph, 'rel_type')
            nx.draw_networkx_edge_labels(self.graph, pos=graph_pos, edge_labels=edge_labels, font_size=3)
        plt.savefig(graph_output_path)

    def __color_paths(self, original_node_colors: dict) -> tuple:
        """Generates color definitions for nodes and edges in graph.

        Parameters
        ----------
        original_node_colors : dict
            Dict mapping node_id to color

        Returns
        -------
        tuple
            Node color array and edge color array.
        """
        flattened_node_set = set()
        involved_edges = set()
        for single_path in self.paths:
            flattened_node_set.update(single_path)
            tupled_edges = [(single_path[i], single_path[i + 1]) for i in range(len(single_path) - 1)]
            involved_edges.update(tupled_edges)
        node_color_mapping = ['purple' if node_id in flattened_node_set else color
                              for node_id, color in original_node_colors.items()]
        edge_color_mapping = ['purple' if pair in involved_edges else 'black' for pair in self.graph.edges()]
        return node_color_mapping, edge_color_mapping

    def shortest_paths(self, source: str, target: str, print_paths: bool = False) -> Optional[list]:
        """Finds the shortest paths between a source node and a target node.

        Parameters
        ----------
        source : str
            HGNC symbol for the starting node.
        target : str
            HGNC symbol for the ending node.
        print_paths : bool
            If True, prints the paths found to STDOUT. Defaults to False.

        Returns
        -------
        Optional[list]
            Returns a list of path lists.
        """
        rev_labels = {metadata[SYMBOL]: node_id for node_id, metadata in self.nodes.items()}
        source_id, target_id = rev_labels[source], rev_labels[target]
        paths = nx.all_shortest_paths(self.graph, source_id, target_id)
        self.paths = [x for x in paths]

        if print_paths:
            for single_path in self.paths:
                START, END = "(START) ", " (END)"
                path_symbols = [self.nodes[node_id] for node_id in single_path]
                path_string = " -> ".join(path_symbols)
                print(START + path_string + END)

        return self.paths


class Statistics(Network):
    """Class for generating statistics about a network."""

    def __init__(self, node_list: str = None, edge_list: str = None, ppi_file: str = None, enrich: bool = False):
        super().__init__(node_list, edge_list, ppi_file, enrich)
        self.sum_stats = None

    def summary_statistics(self) -> None:
        """Generates summary statistics for a network."""
        molecule_counter = {PROTEIN: 0, RNA: 0, DNA: 0}
        for metadata in self.nodes.values():
            molecule_counter[metadata[MOLECULE]] += 1

        sum_stats = {
            'Nodes': sum(molecule_counter.values()),
            'Protein Nodes': molecule_counter[PROTEIN],
            'RNA Nodes': molecule_counter[RNA],
            'DNA Nodes': molecule_counter[DNA],
            'Graph Density': nx.density(self.graph),
            'Average Degree Connectivity': str(nx.average_degree_connectivity(self.graph))
        }

        sum_stats.update(Counter([attr['rel_type'] for _, _, attr in self.graph.edges(data=True)]))
        self.sum_stats = pd.DataFrame({'Stat': list(sum_stats.keys()), 'Value': list(sum_stats.values())})

    def export_stats(self, output_path: str = None):
        """Exports the summary statistics.

        Parameters
        ----------
        output_path : str
            File path to write summary statistics to.

        Raises
        ------
        ValueError
            output_path must end in ".csv", ".tsv" or ".json"
        """
        if self.sum_stats is not None:
            if output_path.endswith(".tsv"):
                self.sum_stats.to_csv(output_path, sep="\t")
            elif output_path.endswith(".csv"):  # Use default option
                self.sum_stats.to_csv(output_path, sep=",")
            elif output_path.endswith(".json"):
                self.sum_stats.to_json(output_path)
            else:
                raise ValueError("Stats output path not csv, tsv, or json!")
