import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys
from sys import argv
import click

@click.command()

@click.argument('path')
@click.option('--source',help='Name of the Source Node [must]')
@click.option('--target',help='Name of the Target Node [must]')
@click.option('-p','--ppi',help='Name of the Protein-Protein Interaction File [optional]',type=click.Path(exists=True),required=False)
@click.option('-n','--nodes',help='Name of the Node File [optional]',type=click.Path(exists=True), required=False)
@click.option('-e','--edges',help='Name of the Edge File [optional]',type=click.Path(exists=True), required=False)
@click.option('--output',help='Name of the Output File')  

def main(path:str,source:str,target:str,ppi:str,nodes:str,edges:str,output:str)->nx.Graph:
    """click function to highlight the shortest path the source and target nodes,
    param source: starting node,
    param target: ending node
    param ppi: PPI file
    param nodes : node file
    param edges: edge file
    param output: output file"""
    def compiling_function_for_shortest_path(source:str,target:str,output:str,nodes:str,edges:str)->nx.Graph:
        """a compiling function to perform shortest path finding
        param source: starting node
        param target : ending node
        param nodes : node file
        param edge : edge file"""
        def finding_the_path(source:str,target:str)->list:
            """function to find the shortest path
            param source :starting node
            param target : ending node
            return: a path if it exits"""
            protein_graph=nx.Graph()
            protein_graph.add_nodes_from(nodes)
            protein_graph.add_edges_from(edges)
            if nx.has_path(protein_graph,source,target):
                return protein_graph,[p for p in nx.all_shortest_paths(protein_graph, source , target )]
            else:
                print("There is no path between {} and {}".format(source,target))
                sys.exit()
                #return "There is no path"

        def highlighting_the_path(path_of_node:list,output:str)->nx.Graph:
            """a function to highlight the shortest path
            param path_of_node: shortest path
            param output: output file
            return : a graph showing the shortest path"""
            graph_pos = nx.spring_layout(protein_graph, k=0.06,)
            plt.figure(figsize=(18, 10))
            nx.draw_networkx(protein_graph, pos=graph_pos,
                             with_labels=True,  node_color='white', alpha=0.3)

            number_of_paths=len(path_of_node)
            print("There are {} paths available between the given nodes between {} and {}".format(number_of_paths,source,target))
            print((path_of_node))

            color=['b','g','y','c','m'] # different colors for highlighting different paths
            for i in range( (number_of_paths)):
                path =  path_of_node[i]
                path_edges = list(zip(path,path[1:]))
                #print(path_edges)
                nx.draw_networkx_nodes(protein_graph,graph_pos,nodelist=path,node_color=color[i])
                nx.draw_networkx_edges(protein_graph,graph_pos,edgelist=path_edges,edge_color=color[i],width=2)
            plt.title("Protein-Protein Interactions and Shortest Path Highlighted Between {} and {}".format(source,target),fontsize=25)
            filename, file_extension = os.path.splitext(output)
            output=filename+'_'+'shortest_path_'+source+'_'+target+file_extension  #custom filename based on source and target
            print("The new custom output filename is {}".format(output))
            plt.savefig(output)
            plt.show()

        #total_nodes,edge_list=reading_the_ppi_file(ppi)
        protein_graph,path=finding_the_path(source,target)
        highlighting_the_path(path,output)
       
    #if ppi file is given
    
    if ppi:
        def reading_the_ppi_file(ppi:str)->list:
            """function for producing edge list and node list
            param ppi: name of the ppi file
            return node list, edge list"""
            ppi_data=pd.read_csv(ppi)
            out_node=ppi_data['out'].unique().tolist()
            in_node=ppi_data['in'].unique().tolist()
            total_nodes= (out_node)+ (in_node)
            total_nodes=list(set(total_nodes))
            total_nodes=sorted(total_nodes)


            edge_list=[]
            for i in  range(len(ppi_data['out'])):
                 edge_list.append((ppi_data['out'][i],ppi_data['in'][i]))
            
            return total_nodes, edge_list
        total_nodes,edge_list=reading_the_ppi_file(ppi)
        compiling_function_for_shortest_path(source,target,output,nodes=total_nodes,edges=edge_list)
    else:        # if edge list file , node list file is directly provided
        list_of_edges=[]
        f_node=pd.read_csv(nodes,sep='\t',header=None) 
        f_edge=pd.read_csv(edges,sep='\t',header=None)
        list_of_nodes = f_node[1]
 
        for i,j in enumerate(f_edge[0]):
            list_of_edges.append((j,f_edge[1][i]))
            
             
        compiling_function_for_shortest_path(source,target,output,nodes=list_of_nodes,edges=list_of_edges)


if __name__ == "__main__":
    main()
     