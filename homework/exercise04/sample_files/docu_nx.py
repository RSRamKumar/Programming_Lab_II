import os
import sys
import click

from typing import Iterable, Tuple, Optional

import networkx as nx
import matplotlib.pyplot as plt


# Read PPI content
def read_ppis(ppi_file_path: str) -> Iterable[Tuple[str]]:
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
    with open(ppi_file_path, 'r') as ppif:
        content = ppif.readlines()
    # Create list of relation tuples
    rels = [tuple(x.strip().split(",")) for x in content[1:]]
    return rels


# Generate unique list of nodes
def create_node_dict(relations: Iterable[Tuple[str]]) -> dict:
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
    nodes = set()
    for rel in relations:
        nodes.add(rel[0])
        nodes.add(rel[2])
    # Make a dictionary relating symbol to identifier
    node_mapper = {symbol: str(index+1) for index, symbol in enumerate(nodes)}
    return node_mapper


# Create node list file
def write_node_list(nodes: dict, node_file_path: str) -> None:
    """Writes unique nodes to a tab separated file with identifier in first column and HGNC symbol in second.

    Parameters
    ----------
    nodes : dict
        Dictionary of unique nodes with their integer identifier as the key and HGNC symbol as the value.
    node_file_path : str
        File path for node list.
    """
    with open(node_file_path, 'w') as node_f:
        for symbol, identifier in nodes.items():
            node_f.write('\t'.join([identifier, symbol]) + '\n')


# Create edge list file
def write_edge_list(relations: Iterable[Tuple[str]], node_mapper: dict, edge_file_path: str) -> None:
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
    with open(edge_file_path, 'w') as edge_f:
        for rel in relations:
            sub, obj = node_mapper[rel[0]], node_mapper[rel[2]]
            rel_type = {'rel_type': rel[1].replace(" ", "_")}  # Replace whitespace
            edge_f.write('\t'.join([sub, obj, str(rel_type)]) + '\n')


# Wrapper function
def compile_files(ppi_file_path: str, node_file_path: str, edge_file_path: str) -> None:
    """Wrapper function for generating node/edge lists from a PPI file."""
    relations = read_ppis(ppi_file_path)
    node_mapper = create_node_dict(relations)
    write_node_list(node_mapper, node_file_path)
    write_edge_list(relations, node_mapper, edge_file_path)


# Generate graph
def import_graph(edge_file_path: str) -> nx.Graph:
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
    g = nx.read_edgelist(edge_file_path, delimiter='\t')
    return g


# Gather the nodes and their labels
def import_node_labels(node_file_path: str, reverse: bool = False) -> dict:
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


# Produce the graph
def generate_graph_image(graph_output_path: str, graph: nx.Graph,
                         node_labels: dict, path_nodes: Optional[list] = None) -> None:
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
    check_output(graph_output_path)  # Do first so you don't waste time

    if path_nodes is not None:
        node_colors, edge_colors = color_paths(graph, path_nodes)
    else:
        node_colors, edge_colors = 'red', 'black'

    plt.figure(figsize=(18, 18))  # initialize figure with size
    graph_pos = nx.spring_layout(graph, k=0.06)
    nx.draw_networkx(graph, pos=graph_pos,
                     with_labels=True,
                     labels=node_labels,
                     node_color=node_colors,
                     edge_color=edge_colors,
                     alpha=0.3)
    plt.savefig(graph_output_path)


def color_paths(graph: nx.Graph, path_nodes: list) -> tuple:
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
        tupled_edges = [(single_path[i], single_path[i+1]) for i in range(len(single_path)-1)]
        involved_edges.update(tupled_edges)
    node_color_mapping = ['blue' if node_id in flattened_node_set else 'red' for node_id in graph.nodes()]
    edge_color_mapping = ['purple' if pair in involved_edges else 'black' for pair in graph.edges()]
    return node_color_mapping, edge_color_mapping


def shortest_paths(source: str, target: str, graph: nx.Graph,
                   node_labels: dict, print_paths: bool = False) -> Optional[list]:
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
    rev_labels = {v: k for k, v in node_labels.items()}
    source_id, target_id = rev_labels[source], rev_labels[target]
    paths = nx.all_shortest_paths(graph, source_id, target_id)
    extracted_paths = [x for x in paths]

    if print_paths:
        for single_path in extracted_paths:
            START, END = "(START) ", " (END)"
            path_symbols = [node_labels[node_id] for node_id in single_path]
            path_string = " -> ".join(path_symbols)
            print(START + path_string + END)

    return extracted_paths


# Start of CLI methods
@click.group(help=f"Network script Command Line Utilities on {sys.executable}")
def main():
    """Entry method."""
    pass


# @main.command()
# @click.argument('ppi')
# @click.argument('output_path')
# def create(ppi: str, output_path: str):
#     """Creates a graph image from a PPI file
#
#     Parameters
#     ----------
#     ppi : str
#         File path to a PPI CSV file.
#     output_path : File path for generated graph image output.
#     """
#     node_path, edge_path = "node_list.tsv", "edge_list.tsv"
#     compile_files(ppi_file_path=ppi, node_file_path=node_path, edge_file_path=edge_path)
#
#     g = import_graph(edge_path)
#     node_mapper = import_node_labels(node_path)
#     generate_graph_image(graph_output_path=output_path, graph=g, node_labels=node_mapper)


@main.command()
@click.option('-p', '--ppi', default=None, help="A CSV file containing PPIs.")
@click.option('-n', '--nodes', default=None, help="A TSV file containing defined nodes of a network.")
@click.option('-e', '--edges', default=None, help="A TSV file containing defined edges of a network.")
@click.argument('output_path')
def create(ppi: str, nodes: str, edges: str, output_path: str):
    """Creates a graph image from a PPI file or node+edge lists."""
    if ppi and nodes and edges:
        raise IOError("Cannot import all 3!")

    if ppi:
        node_path, edge_path = "node_list.tsv", "edge_list.tsv"
        compile_files(ppi_file_path=ppi, node_file_path=node_path, edge_file_path=edge_path)

    else:
        node_path, edge_path = nodes, edges

    g = import_graph(edge_path)
    node_mapper = import_node_labels(node_path)
    generate_graph_image(graph_output_path=output_path, graph=g, node_labels=node_mapper)


@main.command()
@click.option('-s', '--source', help="HGNC symbol for the starting/source node.")
@click.option('-t', '--target', help="HGNC symbol for the ending/target node.")
@click.argument('output_path')
@click.option('-p', '--ppi', default=None, help="A CSV file containing PPIs.")
@click.option('-n', '--nodes', default=None, help="A TSV file containing defined nodes of a network.")
@click.option('-e', '--edges', default=None, help="A TSV file containing defined edges of a network.")
@click.option('-v', '--verbose', default=False, is_flag=True, help="When used, will print the paths to STDOUT.")
def path(source: str, target: str, ppi: str, nodes: str, edges: str, output_path: str, verbose: bool):
    """Generates a graph image highlighting specific paths between the given source and target."""
    if ppi and nodes and edges:
        raise IOError("Cannot import all 3!")

    if ppi:
        node_path, edge_path = "node_list.tsv", "edge_list.tsv"
        compile_files(ppi_file_path=ppi, node_file_path=node_path, edge_file_path=edge_path)

    else:
        node_path, edge_path = nodes, edges

    g = import_graph(edge_path)
    node_mapper = import_node_labels(node_path)
    sp = shortest_paths(source, target, g, node_mapper, print_paths=verbose)
    generate_graph_image(graph_output_path=output_path, graph=g, node_labels=node_mapper, path_nodes=sp)


if __name__ == "__main__":
    main()
