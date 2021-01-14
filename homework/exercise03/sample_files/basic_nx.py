import os
import sys

import networkx as nx
import matplotlib.pyplot as plt


# Read PPI content
def read_ppis(ppi_file_path):
    with open(ppi_file_path, 'r') as ppif:
        content = ppif.readlines()
    # Create list of relation tuples
    rels = [tuple(x.strip().split(",")) for x in content[1:]]
    return rels


# Generate unique list of nodes
def create_node_dict(relations):
    nodes = set()
    for rel in relations:
        nodes.add(rel[0])
        nodes.add(rel[2])
    # Make a dictionary relating symbol to identifier
    node_mapper = {symbol: str(index+1) for index, symbol in enumerate(nodes)}
    return node_mapper


# Create node list file
def write_node_list(nodes, node_file_path):
    with open(node_file_path, 'w') as node_f:
        for symbol, identifier in nodes.items():
            node_f.write('\t'.join([identifier, symbol]) + '\n')


# Create edge list file
def write_edge_list(relations, node_mapper, edge_file_path):
    with open(edge_file_path, 'w') as edge_f:
        for rel in relations:
            sub, obj = node_mapper[rel[0]], node_mapper[rel[2]]
            rel_type = {'rel_type': rel[1].replace(" ", "_")}  # Replace whitespace
            edge_f.write('\t'.join([sub, obj, str(rel_type)]) + '\n')


# Wrapper function
def compile_files(ppi_file_path, node_file_path, edge_file_path):
    relations = read_ppis(ppi_file_path)
    node_mapper = create_node_dict(relations)
    write_node_list(node_mapper, node_file_path)
    write_edge_list(relations, node_mapper, edge_file_path)


# Generate graph
def import_graph(edge_file_path) -> nx.Graph:
    g = nx.read_edgelist(edge_file_path, delimiter='\t')
    return g


# Gather the nodes and their labels
def import_node_labels(node_file_path):
    with open(node_file_path, 'r') as node_f:
        content = node_f.readlines()
    nodes = dict()
    for pair in content:
        identifier, symbol = pair.strip().split("\t")
        nodes[identifier] = symbol
    return nodes


# Produce the graph
def generate_graph(graph_output_path, edge_list, node_list):
    graph = import_graph(edge_list)
    node_labels = import_node_labels(node_list)  # compile node labels
    plt.figure(figsize=(18, 18))  # initialize figure with size
    graph_pos = nx.spring_layout(graph, k=0.06)
    nx.draw_networkx(graph, pos=graph_pos,
                     with_labels=True, labels=node_labels, node_color='red', alpha=0.3)
    # plt.show()
    plt.savefig(graph_output_path)


if __name__ == "__main__":
    ppi_file = sys.argv[1]
    output_path = sys.argv[2]
    node_path, edge_path = "node_list.tsv", "edge_list.tsv"
    compile_files(ppi_file_path=ppi_file, node_file_path=node_path, edge_file_path=edge_path)
    generate_graph(graph_output_path=output_path, edge_list=edge_path, node_list=node_path)

    # Delete meta files from user's computer
    os.remove(node_path)
    os.remove(edge_path)
