import os 
from sys import argv
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pylab import rcParams
import pprint
os.chdir(r'C:\Users\Ram Kumar R S\Desktop\plab2ws20-ruppasur\Exercise-02')

  
def producing_network_graph(input_file):
     """ function to generate the network graph file
     Arg: input protein protein interaction file
     Return: pdf version of the network graph"""

     print("Reading the input file:",input_file)
     ppi_data=pd.read_csv(input_file)
 
     out_node=ppi_data['out'].unique().tolist()
     in_node=ppi_data['in'].unique().tolist()
    
    # creating the total nodes
     total_nodes= (out_node)+ (in_node)
     total_nodes=list(set(total_nodes))
     total_nodes=sorted(total_nodes)
    
    # assigning node identifier
     node_list={(i+1): total_nodes[i] for i in range(len(total_nodes))}
 
    # writing the output node file 
     with open('node_list.tsv','w') as f:
        for node in node_list:
            f.write("{}\t{}\n".format(node, node_list[node]))
 
 
     edge_list=[]
     node_list_inv={j:i for i,j in node_list.items()}
     for i in  range(len(ppi_data['out'])):
       edge_list.append((node_list_inv[ ppi_data['out'][i]],node_list_inv[ ppi_data['in'][i]] ,ppi_data['interaction_type'][i]))
 
    
    # writing the output edge file 
     edge_list_no_metadata=[(i[0],i[1]) for i in edge_list]
     with open('edge_list_no_metadata.tsv','w') as f:          # writing with no metadata
       for edge in edge_list_no_metadata:
         f.write("{}\t{}\n".format( *edge ))
 
 
     def drawing_graph_from_edge_list(edge_file_path:str)->nx.Graph:
        """function to produce a network graph
        input: file path/file name containing the edge information
        output: graph"""
        graph=nx.read_edgelist(edge_file_path,delimiter='\t')
        return graph
              
     def graph_node_labels(node_file_path:str)->dict:
        """funtion to generate the dict version of the node list
        arg: node list file path
        return : dictionary version of it"""
        f = open(node_file_path,'r') 
        interactions= f.readlines()
        nodes_dict= {}
        for pair in interactions:
            identifier,node=pair.strip().split('\t')
            nodes_dict[identifier]=node
        return nodes_dict
        
    
     def generate_graph( edge_list ,node_list ,output_file):
        """function to generate pdf graph network file
        Arg 1- path of edge list file
        Arg 2- path of node list file
        Arg 3- path of output graph file
        Return - pdf version of the network graph """
        graph=drawing_graph_from_edge_list(edge_list)
        graph_pos=nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, graph_pos,node_color='red')#,alpha=0.5)
        nx.draw_networkx_edges(graph,graph_pos)
        node_labels= graph_node_labels(node_list)
        nx.draw(graph, labels=node_labels,with_labels=True,font_size=20)
        #nx.draw_networkx_labels(node_list, pos = nx.spring_layout(node_list), font_size = 20, with_labels = True);
        plt.savefig(output_file)
        plt.title("Protein Protein Interactions  ",fontsize=100)
        plt.show()    
         
     print("Generating the output graph file:",output_file)
     generate_graph( 'edge_list_no_metadata.tsv','node_list.tsv',output_file)
    
if __name__ == "__main__":
    script,input_file,output_file=argv
    producing_network_graph(input_file)
    