import os
import sys
import click

from typing import Iterable, Tuple, Optional

import networkx as nx
import matplotlib.pyplot as plt

from pathlib import Path
import os
import click


class Network():
    def __init__(self, csv_file: str = None, edgelist: str = None, nodelist: str = None):
        self.csv_file = csv_file
        self.edgelist = edgelist
        self.nodelist = nodelist
        if self.csv_file and self.nodelist and self.edgelist:
            raise IOError("Cannot import all 3!")
        self.relation = None
        self.nodes = None
        self.graph = None

    def read_ppis(self: str) -> Iterable[Tuple[str]]:
        """Reads a file of PPIs.

        Parameters
        ----------
        ppi_file_path : str
            Path to the PPI file.

        Returns
        -------
        rels : Iterable[Tuple[str]]
            List of individual relationships found in PPI file.
        """
        with open(self.csv_file, 'r') as ppif:
            content = ppif.readlines()
        # Create list of relation tuples
        rels = [tuple(x.strip().split(",")) for x in content[1:]]
        self.relation = rels
        return rels

    def create_node_dict(self: str) -> dict:
        """Generates a dictionary mapping unique integer identifiers to HGNC symbols extracted from PPI relationship list.

        Parameters
        ----------
        relations : Iterable[Tuple[str]]
            List of individual relationships found in PPI file.

        Returns
        -------
        node_mapper : dict
            Dictionary of unique nodes with their integer identifier as the key and HGNC symbol as the value.
        """
        self.read_ppis()
        nodes = set()
        for rel in self.relation:
            nodes.add(rel[0])
            nodes.add(rel[2])
        # Make a dictionary relating symbol to identifier
        node_mapper = {symbol: str(index + 1) for index, symbol in enumerate(nodes)}
        self.nodes = node_mapper
        return node_mapper

    def write_node_list(self, node_file_path: str) -> None:
        """Writes unique nodes to a tab separated file with identifier in first column and HGNC symbol in second.

        Parameters
        ----------
        nodes : dict
            Dictionary of unique nodes with their integer identifier as the key and HGNC symbol as the value.
        node_file_path : str
            File path for node list.
        """
        self.read_ppis()
        self.create_node_dict()
        with open(node_file_path, 'w') as node_f:
            for symbol, identifier in self.nodes.items():
                node_f.write('\t'.join([identifier, symbol]) + '\n')

    def write_edge_list(self, edge_file_path: str) -> None:
        """Writes the edge relations to a tab separated file.

        Parameters
        ----------
        relations : list
            List of individual relationships as tuples: (node1_id, relationship, node2_id)
        node_mapper : dict
            Dictionary of unique nodes with their integer identifier as the key and HGNC symbol as the value.
        edge_file_path : str
            File path for edge list.
        """
        self.read_ppis()
        self.create_node_dict()
        with open(edge_file_path, 'w') as edge_f:
            for rel in self.relation:
                sub, obj = self.nodes[rel[0]], self.nodes[rel[2]]
                rel_type = {'rel_type': rel[1].replace(" ", "_")}  # Replace whitespace
                edge_f.write('\t'.join([sub, obj, str(rel_type)]) + '\n')

    def import_graph(self, edge_file_path: str) -> nx.Graph:
        """Generate a NetworkX graph from an edge list file.

        Parameters
        ----------
        edge_file_path : str
            File path for edge list.

        Returns
        -------
        nx.Graph
            NetworkX graph.
        """
        my_file = Path(edge_file_path)

        if my_file.exists() == False:
            self.write_edge_list(edge_file_path)
        g = nx.read_edgelist(edge_file_path, delimiter='\t')
        self.graph = g

    def import_node_labels(self, node_file_path: str, reverse: bool = False) -> dict:
        """Reads the nodes identifier/HGNC symbol from a node list file.

        Parameters
        ----------
        node_file_path : str
            File path for node list.
        reverse : bool
            If True, sets HGNC symbols as keys and node ID as value.

        Returns
        -------
        nodes : dict
            Dictionary of unique nodes with their integer identifier as the key and HGNC symbol as the value.
        """
        my_file = Path(node_file_path)

        if my_file.exists() == False:
            self.write_node_list(node_file_path)

        with open(node_file_path, 'r') as node_f:
            content = node_f.readlines()
        nodes = dict()
        for pair in content:
            identifier, symbol = pair.strip().split("\t")

            if reverse:
                nodes[symbol] = identifier

            else:
                nodes[identifier] = symbol
        return nodes

    def compile_(self, node_file_path, edge_file_path):
        """Wrapper function for generating node/edge lists from a PPI file."""
        self.write_node_list(node_file_path)
        self.write_edge_list(edge_file_path)


class Analyzer(Network):
    def __init__(self, csv_file=None, edgelist=None, nodelist=None):
        super().__init__(csv_file, edgelist, nodelist)

    @staticmethod
    def check_output(graph_output_path: str) -> None:
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

    def color_paths(self, path_nodes: list) -> tuple:
        """Generates color definitions for nodes and edges in graph.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph compiled from an edge list.
        path_nodes : list
            List of path lists.

        Returns
        -------
        tuple
            Node color array and edge color array.
        """
        flattened_node_set = set()
        involved_edges = set()
        for single_path in path_nodes:
            flattened_node_set.update(single_path)
            tupled_edges = [(single_path[i], single_path[i + 1]) for i in range(len(single_path) - 1)]
            involved_edges.update(tupled_edges)
        node_color_mapping = ['blue' if node_id in flattened_node_set else 'red' for node_id in self.graph.nodes()]
        edge_color_mapping = ['purple' if pair in involved_edges else 'black' for pair in self.graph.edges()]
        return node_color_mapping, edge_color_mapping

    def generate_graph_image(self, graph_output_path: str, edgefile_path, path_nodes: Optional[list] = None,relation:bool=False) -> None:
        """Creates an image of a network compiled from NetworkX graph and node dictionary.

        Parameters
        ----------
        graph_output_path : str
            Path to output the generated graph image.
        graph : nx.Graph
            NetworkX graph compiled from an edge list.
        node_labels : dict
            Dictionary relating node IDs to HGNC symbols.
        path_nodes : list
            List of path lists.
        """
        self.read_ppis()
        self.create_node_dict()
        self.check_output(graph_output_path)  # Do first so you don't waste time
        self.import_graph(edgefile_path)
        if path_nodes is not None:
            node_colors, edge_colors = self.color_paths(self.graph, path_nodes)
        else:
            node_colors, edge_colors = 'red', 'black'
        labels = {v: k for k, v in self.nodes.items()}
        plt.figure(figsize=(30, 30))  # initialize figure with size
        graph_pos = nx.spring_layout(self.graph, k=0.06)
        nx.draw_networkx(self.graph, pos=graph_pos,
                         with_labels=True,
                         labels=labels,
                         node_color=node_colors,
                         edge_color=edge_colors,
                         alpha=0.5)

        if relation:
            grafo_labels = nx.get_edge_attributes(self.graph, "rel_type")
            nx.draw_networkx_edge_labels(self.graph, pos=graph_pos , edge_labels=grafo_labels,label_pos=0.5,font_size=5)
        plt.savefig(graph_output_path)
        plt.show()


    def shortest_paths(self, source: str, target: str, edgefile_path, print_paths: bool = False) -> Optional[list]:
        """Finds the shortest paths between a source node and a target node.

        Parameters
        ----------
        source : str
            HGNC symbol for the starting node.
        target : str
            HGNC symbol for the ending node.
        graph : nx.Graph
            NetworkX graph compiled from an edge list.
        node_labels : dict
            Dictionary relating node IDs to HGNC symbols.
        print_paths : bool
            If True, prints the paths found to STDOUT. Defaults to False.

        Returns
        -------
        Optional[list]
            Returns a list of path lists.
        """
        self.read_ppis()
        self.create_node_dict()
        #         self.check_output(graph_output_path)  # Do first so you don't waste time
        self.import_graph(edgefile_path)

        rev_labels = {v: k for k, v in self.nodes.items()}
        source_id, target_id = self.nodes[source], self.nodes[target]
        paths = nx.all_shortest_paths(self.graph, source_id, target_id)
        extracted_paths = [x for x in paths]

        if print_paths:
            for single_path in extracted_paths:
                START, END = "(START) ", " (END)"
                path_symbols = [rev_labels[node_id] for node_id in single_path]
                path_string = " -> ".join(path_symbols)
                print(START + path_string + END)


# Start of CLI methods
@click.group()
def main():
    pass


@main.command()
@click.option('-p', '--csv_file', type=click.Path(exists=True), help='CSV file containing protein protein interaction')
@click.option('-n', '--nodelist', help='tab seperated file of unique id and nodes eg: 1-->HGNC')
@click.option('-e', '--edgelist', help='edge list eg: out-node-->in-node-->physical association')
def compile(csv_file=None, edgelist=None, nodelist=None) -> None:
    obj=Network(csv_file)
    obj.compile_(nodelist,edgelist)

@main.command()
@click.option('-o', '--outfile', help='edge list eg: out-node-->in-node-->physical association')
@click.option('-p', '--csv_file', type=click.Path(exists=True), help='CSV file containing protein protein interaction')
@click.option('-e', '--edgelist', help='edge list eg: out-node-->in-node-->physical association')
@click.option('-n', '--nodelist', help='tab seperated file of unique id and nodes eg: 1-->HGNC')
@click.option('-r', '--relation',type=bool ,help='edge list eg: out-node-->in-node-->physical association')

def create(outfile,csv_file=None, edgelist=None, nodelist=None,relation=False):
    obj2=Analyzer(csv_file)
    obj2.generate_graph_image(outfile,edgefile_path=edgelist,relation=False)

if __name__ == '__main__':
    main()

#I have tried this in pycharm
#python exe_4.py create -o"con.png"  -p"ppis.csv" -e"t_e.tsv" -n"t_n.tsv" -rTrue
#python exe_4.py compile -p "ppis.csv" -n "t_n.tsv" -e "t_e.tsv"






# @click.group()
# @click.option('--ppis')
#
# @click.pass_context
# def cli(ctx, ppis):
#     ctx.obj = Network(ppis)
#
# @cli.command()
# @click.option('--node_file_path')
# @click.option('--edge_file_path')
# @click.pass_obj
# def compile(node_file_path, edge_file_path):
#     ctx.obj.write_node_list(node_file_path)
#     ctx.obj.write_edge_list(edge_file_path)
#     ctx.obj.
