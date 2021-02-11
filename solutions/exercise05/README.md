# PLAB2WS20-RuppaSur

This Readme file contains information regarding the Assignment 05 submission. 

1. 'Task 1' and 'Task 2' about the creation of the files/folders is done

2. For 'Task 3' instead of using `request` library, `http2 library` is used for API request. I had some issue in JSON file retreival. 

3. For 'Task 4', the `utils.py` contains the downloading and retrieving methods.
Sample Implementation:
python utils.py info --hgnc_symbol "CRP"

4. For 'Task 5':
	1. Two methods called **collecting_identifier_from_API** and **generating_enriched_node_file** does the enrichment job in the **network_ex05.py** . 
Sample Implementation:
```python
	  h= Network(ppi_file="ppis_sample.csv") 
	  h.generating_enriched_node_file()
 (or)
	   e=Network(node_list="node_sample.tsv",edge_list="new_edge_list.tsv")
	  (e.generating_enriched_node_file())
```

	2. Producing Enriched Node dataset

My *enriched_node_file.tsv* looks this manner: 

|           |       |                  |             |                                                  |
|-----------|------ |------------------|-------------|------------------------------------------------- |
| KAT6A     |13013  | ENSG00000083168  | ['Q92794']  | http://rest.genenames.org/fetch/symbol/KAT6A     |
|MIRLET7E   | 8016  |ENSG00000198972   |None         | http://rest.genenames.org/fetch/symbol/MIRLET7E  |

 
 Certain genes like **MIRLET7E** , **MIR34A** have no Uniprot Id , hence mentioned as None. 
 
 I initially tested part by part of the dataset, then whole dataset found that there are certain genenames not found in the database like **TWISTNB** , hence removed from the enriched_node_file.
 Sufficient logging info and warning messages are provided.
 When implementation of the network scrpit with the logging, the log file is flooded with the **matplotlib** messages.

	3. Create CLI command - Not implemented

Thank you!