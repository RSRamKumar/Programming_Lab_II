import os
import sys

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Iterable, Union
import warnings
warnings.filterwarnings("ignore")             # to remove some warnings
import click

@click.command()
@click.argument('create') 
@click.argument('input_file_path', type=click.Path(exists=True))
@click.argument('output_file_path')  

def main(create:str,input_file_path:str,output_file_path:str)->nx.Graph:
    """click function to perform CLI task in generating a network graph,
    param create: label of the CLI command,
    param input_file_path : name of the PPI file,
    param output_file_path : name of the output file,
    return : network graph"""

    def reading_the_file(input_file_path:str)->List[str]:
        """function to return the node list
        param input_file_path: input protein protein interaction file
        return: list of nodes in the input file""" 

        ppi_data=pd.read_csv(input_file_path)
        out_node=ppi_data['out'].unique().tolist()
        in_node=ppi_data['in'].unique().tolist()

         # creating the total nodes
        total_nodes= (out_node)+ (in_node)
        total_nodes=list(set(total_nodes))
        total_nodes=sorted(total_nodes)

        return total_nodes

    def producing_node_identifier(nodes:List[str])-> dict:
        """function to assign an unique identifier to the nodes
        param nodes: list of nodes in the PPI file
        return: dict containing node,identifier pair"""

        # assigning node identifier
        node_list={(index+1): node for index,node in enumerate(nodes)}
        return node_list

    def generating_node_file(node_list:dict,node_file_path:str)->None:
        """function to write the node identifier to the output file
        param node_list: node,identifier pair
        param node_list_path: name of the file
        """
        with open(node_file_path,'w') as f:
            for node in node_list:
                f.write("{}\t{}\n".format(node, node_list[node]))


    def producing_edge_identifer(input_file_path:str,node_list:dict)->list:
        """"function to generate edge identifier (replacing hgnc nodes with identifier)
        param input_file_path: protein protein interaction file
        param node_list: identifier,node pair
        return edge list with identifiers"""
        edge_list=[]
        node_list_inv={j:i for i,j in node_list.items()}
        ppi_data=pd.read_csv(input_file_path)
        for i in  range(len(ppi_data['out'])):
            edge_list.append((node_list_inv[ ppi_data['out'][i]],node_list_inv[ ppi_data['in'][i]]   ,ppi_data['interaction_type'][i]))
        return edge_list

    def generating_edge_file(edge_list_path:str,edge_list:list)->None:
        """"function to write the edge list to the output
        param edge_list_path: name of the file
        param edge_list: edge list with identifiers"""
        with open(edge_list_path,'w') as f:
            for edge in edge_list:                      # writing no metadata
                f.write("{}\t{}\n".format( edge[0],edge[1] ))


    def compile_function(input_file_path:str,node_file_path:str,edge_file_path:str)->None:
        """function to call the above functions
        param input_file_path : input protein protein interaction file
        param node_file_path : output node file name
        param edge_file_path : output edge file name"""
        node_data = reading_the_file(input_file_path)
        node_list = producing_node_identifier(node_data)
        generating_node_file(node_list,node_file_path) 
        edge_list=producing_edge_identifer(input_file_path,node_list)
        generating_edge_file(edge_file_path,edge_list)


    def drawing_graph_from_edge_list(edge_file_path:str)->nx.Graph:
        """function to generate a graph from edge list file
        param edge_file_path: file name of the edge file
        return : network graph generated from the file"""
        graph=nx.read_edgelist(edge_file_path,delimiter='\t')
        return graph

    def import_node_labels(node_file_path):
        """function to generate identifier, node pair
        param node_file_path : name of the node file
        return dict containing the identifier, node pair"""
        with open(node_file_path, 'r') as node_f:
            content = node_f.readlines()
        nodes = dict()
        for pair in content:
            identifier, symbol = pair.strip().split("\t")
            nodes[identifier] = symbol
        return nodes


    def generate_graph(graph_output_path:str, edge_list:str, node_list:str)->nx.Graph:
        """function to generate the graph and style it based on the requirements
        param graph_output_path : name of the output file
        param edge_list : name of the edge list file
        param node_list : name of the node list file
        """
        graph = drawing_graph_from_edge_list(edge_list)
        node_labels = import_node_labels(node_list)  # compile node labels
        plt.figure(figsize=(18, 10))  # initialize figure with size
        graph_pos = nx.spring_layout(graph, k=0.06)
        nx.draw_networkx(graph, pos=graph_pos,
                         with_labels=True, labels=node_labels, node_color='red', alpha=0.3)
        # plt.show()
        plt.title("Protein Protein Interactions Visualized",fontsize=30)
        plt.savefig(graph_output_path)
    
    
    
    
    filename, file_extension = os.path.splitext(output_file_path)
    if file_extension in [".docx", ".txt"]:
        print("This '.docx' and '.txt' format is not acceptable, prefer using .pdf , .png, .jpeg")
        sys.exit()
      
    
    node_file_path, edge_file_path = "node_list.tsv", "edge_list.tsv"
    compile_function(input_file_path,node_file_path,edge_file_path)

    generate_graph(graph_output_path=output_file_path, edge_list=edge_file_path, node_list=node_file_path)


if __name__ == "__main__":
    
    main()
    
    # Delete meta files from user's computer
    #os.remove(node_file_path)
    #os.remove(edge_file_path)
