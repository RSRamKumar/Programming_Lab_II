import networkx as nx
import matplotlib.pyplot as plt
import os
from typing import Iterable, Tuple, Optional
#os.chdir(r'C:\Users\Ram Kumar R S\Desktop\plab2ws20-ruppasur\exercise03')
import pandas as pd
import click
import numpy as np
import logging
import startup
from utils import downloading_from_API,extracting_identifiers
import time
from tqdm import tqdm


class Network:
    def __init__(self,ppi_file:str = None, node_list: str= None, edge_list : str=None):
        self.ppi_file=ppi_file
        self.node_list=node_list
        self.edge_list=edge_list
        self.nodes= {}
        self.graph=None

        if ppi_file and (edge_list and node_list):
            logging.warning("All the 3 files are imported, Kindly Import PPI file or Edge and Node file alone!")
            raise ImportError("All the 3 files are imported, Kindly Import PPI file or Edge and Node file alone!")

    def read_ppis(self) -> list:
        """
        Reads the PPI file
        :return:
        list of individual relationship found in the PPI file
        """
        #logging.info("PPI file is passed as an input.")
        if self.ppi_file is not None:
            with open(self.ppi_file, 'r') as ppif:
                content = ppif.readlines()
            return [tuple(x.strip().split(",")) for x in content[1:]]
        else:
            raise ValueError("No PPI file loaded!")

    def create_node_dict(self) -> dict:
        """Generates a dictionary mapping unique integer identifiers to HGNC symbols extracted from PPI relationship list.
        Returns
        -------
        node_mapper : dict
            Dictionary of unique nodes with their integer identifier as the key and HGNC symbol as the value.
        """
        self.relation = self.read_ppis()
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
        ----------.
        node_file_path : str
            File path for node list.
        """
        if self.ppi_file is not None:
            self.read_ppis()
            self.create_node_dict()
            with open(node_file_path, 'w') as node_f:
                for symbol, identifier in self.nodes.items():
                    node_f.write('\t'.join([identifier, symbol]) + '\n')
            print("Node list file is written in the file named '{}'.".format(node_file_path))
        else:
            raise ValueError("No PPI file loaded! to write a node file")

    def write_edge_list(self, edge_file_path: str) -> None:
        """Writes the edge relations to a tab separated file.

        Parameters
        ----------
        edge_file_path : str
            File path for edge list.
        """
        if self.ppi_file is not None:
            self.read_ppis()
            self.create_node_dict()
            with open(edge_file_path, 'w') as edge_f:
                for rel in self.relation:
                    sub, obj = self.nodes[rel[0]], self.nodes[rel[2]]
                    rel_type = {'rel_type': rel[1].replace(" ", "_")}  # Replace whitespace
                    edge_f.write('\t'.join([sub, obj, str(rel_type)]) + '\n')
            print("Edge list file is written in the file named '{}'.".format(edge_file_path))
        else:
            raise ValueError("No PPI file loaded! to write an Edgefile")


    def import_graph(self,edge_file_path: str) -> None:
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
        if os.path.exists(edge_file_path)==False:
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
        if os.path.exists(node_file_path)==False :
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


    def compile_files(self, node_file_path: str, edge_file_path: str) -> None:
        """Wrapper function for generating node/edge lists from a PPI file."""
        self.edge_file_path=edge_file_path
        self.node_file_path=node_file_path
        self.write_node_list(node_file_path)
        self.write_edge_list(edge_file_path)
        logging.info("PPI file was passed and the new node and edge list is generated and placed in the locations {} and {}".format(node_file_path,edge_file_path))

    @staticmethod
    def check_output_format(graph_output_path: str) -> None:
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
            logging.warning("The graph file extension is not acceptable.")


    def generate_graph_image(self,graph_output_path: str ,printing_edge_relationship=False) -> None:
        """Creates an image of a network compiled from NetworkX graph and node dictionary.

        Parameters
        ----------
        graph_output_path : str
            Path to output the generated graph image.
        printing_edge_relationship : False
            Option to print the edge labels in the graph
        """
        self.check_output_format(graph_output_path)
        if self.ppi_file is not None:
            self.nodes=self.create_node_dict()
            self.nodes={j:i for i,j in self.nodes.items()}
            self.import_graph(self.edge_file_path)

        else:
            self.import_graph(self.edge_list)
            self.nodes=self.import_node_labels(self.node_list)
        plt.figure(figsize=(18, 18))  # initialize figure with size
        graph_pos = nx.spring_layout(self.graph, k=0.06)
        nx.draw_networkx(self.graph, pos=graph_pos,
                         with_labels=True,
                         labels=self.nodes,
                         node_color='red',
                          alpha=0.3)

        if printing_edge_relationship ==True:
            grafo_labels = nx.get_edge_attributes(self.graph, "rel_type")
            nx.draw_networkx_edge_labels(self.graph, pos=graph_pos , edge_labels=grafo_labels,label_pos=0.5,font_size=5)
            print("The networkx is stored as {} with the edge labels.".format(graph_output_path))
            plt.savefig(graph_output_path)
        else:
            print("The networkx is stored as {}".format(graph_output_path))
            plt.savefig(graph_output_path)
        logging.info("The graph image was generated and stored in the location {}".format(graph_output_path))

    def collecting_identifier_from_API(self):
        """function to retrieve the information from API for all nodes"""
        identifier_dict={}
        if self.ppi_file is not None:
            self.compile_files("new_node_list.tsv", "new_edge_list.tsv")  # building new files

        elif (self.node_list and self.edge_list) is not None:
            self.nodes= self.import_node_labels(self.node_list,reverse=True)
        for i in tqdm(self.nodes.keys()):
            identifier_dict[i] = extracting_identifiers(i)
            time.sleep(1.0)
        return identifier_dict

    def generating_enriched_node_file(self):
        """function to write the API retreived information to a .TSV file"""
        self.id_dict= self.collecting_identifier_from_API()

        f = open("enriched_node_file.tsv","w")
        for k,v in self.id_dict.items():     #k = 'STX8', v=({'STX8': ('HGNC:11443', 'ENSG00000170310', ['Q9UNK0'])}, 'http://rest.genenames.org/fetch
            if v != None:
                details, link = v
                symbol,b=*(details.keys()),*(details.values())
                #print(symbol)
                hgnc,ensembl,uniprot=b
                #print(hgnc,ensembl,uniprot,link)
                f.write("{},{},{},{},{}\n".format(symbol,hgnc.split(":")[1],ensembl,uniprot,link))
            elif v==None:  # eg TWISTNB : None
                logging.warning("The gene {}  information is not present in the database and discarded from the outputfile.".format(k))
        logging.info("The retrieved data for enrichment is written in the file called 'enriched_node_file.tsv'")

class Analyzer(Network):
    def __init__(self, ppi_file=None,  node_list=None,edge_list=None,source=None,target=None):
        super().__init__(ppi_file,  node_list,edge_list,)
        self.source=source
        self.target=target

    def shortest_path(self):
        """function for returning the shortest path between 2 nodes"""

        if self.ppi_file is not None:  #ppi file provided
            print("New Edge and Node files are generated from PPI file")
            self.compile_files("new_node_list.tsv","new_edge_list.tsv")   #building new files
            self.import_graph("new_edge_list.tsv")
        else:  #edge and node file provided
            self.import_graph(self.edge_list)

        rev_labels = {v: k for k, v in self.nodes.items()}
        source_id, target_id = self.nodes[self.source], self.nodes[self.target]
        paths = nx.all_shortest_paths(self.graph, source_id, target_id)
        extracted_paths = [x for x in paths]
        if extracted_paths == []:
            logging.warning("No shortest path exists between {} and {}".format(self.source,self.target))
        for single_path in extracted_paths:
            START, END = "(START) ", " (END)"
            path_symbols = [rev_labels[node_id] for node_id in single_path]
            path_string = " -> ".join(path_symbols)
            print(START + path_string + END)

class Statistics (Network):
    def __init__(self,ppi_file:str=None,node_list:str=None,edge_list:str=None):
        super().__init__(ppi_file ,node_list ,edge_list )

    def summary_statistics(self)->pd.DataFrame:
        """function to return the summary statistics
        :return pandas dataframe"""
        if self.ppi_file is not None:  #ppi file provided
            #self.read_ppis()
            #self.create_node_dict()
            self.compile_files("new_node_list.tsv","new_edge_list.tsv") #building new files
            self.import_graph("new_edge_list.tsv")
        else:  #edge and node file provided
            self.import_graph(self.edge_list)
        network_dict = {'number_of_nodes': nx.number_of_nodes(self.graph),
                        'number_of_edges': nx.number_of_edges(self.graph),
                        'density': nx.density(self.graph),
                        'average_degree_connectivity': np.mean(
                            np.array(list(nx.average_degree_connectivity(self.graph).values())))}
        network_df = pd.DataFrame(network_dict.values(), index=network_dict.keys(), columns=['Values'])
        return network_df

    def export_stats(self,output_file_name, JSON = False,delimiter = False):
        """function to export the dataframe to an output file
        output_file_name: name of the output file name
        JSON: flag to choose the output as json file
        delimiter: sep for file extension if the file is not a json file"""
        statistics=self.summary_statistics()
        if JSON==True:
            statistics.to_json(output_file_name)
            print("Saving the file in the JSON file")
        else:
            if delimiter==',':
                print("Saving the file in the comma delimited file")
                statistics.to_csv(output_file_name )
            if delimiter=='\t':
                statistics.to_csv(output_file_name,sep='\t')
                print("Saving the file in the tab delimited file")


#Sample Implementations

#h= Network(ppi_file="ppis.csv",node_list="pycharm_node_sample.tsv",edge_list="pycharm_node_sample.tsv") #works fine"""

#h= Network(ppi_file="ppis_sample.csv")#works fine
#h.compile_files("Node_sample.tsv","Edge_sample.tsv")
#h.generate_graph_image("Graph.pdf",printing_edge_relationship=True)

#h= Network(ppi_file="ppis_sample.csv")#works fine
#print(h.collecting_identifier_from_API())
#(h.generating_enriched_node_file())
#print(h.id_dict)
#e=Network(node_list="new_node_list.tsv",edge_list="new_edge_list.tsv")
#(e.generating_enriched_node_file())
#e.generate_graph_image("Graphh.pdf",printing_edge_relationship=False)

#sp=Analyzer(ppi_file="ppis.csv",source="TRA2B",target='CREBBP')
#sp=Analyzer(node_list="new_node_list.tsv",edge_list="new_edge_list.tsv")
#sp.shortest_path()

#s=Statistics(ppi_file="ppis.csv")
#print(s.summary_statistics())
#s=Statistics(edge_list="Edge_sample.tsv",node_list="node_sample.tsv")
#s.export_stats(delimiter=',',output_file_name="output.csv")
#s.export_stats("output.json",JSON=True)
#s.export_stats(delimiter='\t',output_file_name="output.tsv")