import httplib2 as http
import json
import logging
import startup
import os
import click
import sys

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

# part of the code taken from the https://www.genenames.org/help/rest/#!/#tocAnchor-1-1
def downloading_from_API(hgnc_symbol):
    logging.info("The gene symbol under retreival is {}.".format(hgnc_symbol))
    if os.path.exists(os.path.join(startup.data_path,hgnc_symbol+'.json')):
        logging.info("The information about the gene {} is already downloaded!".format(hgnc_symbol))
        return None,None
        #sys.exit()
    else:
        headers = {'Accept': 'application/json'}
        uri = 'http://rest.genenames.org'
        path = '/fetch/symbol/{}'.format(hgnc_symbol)
        target = urlparse(uri+path)
        method = 'GET'
        body = ''
        h = http.Http()
        response, content = h.request(target.geturl(),method,body,headers)
        if response['status'] == '200':
             data = json.loads(content)
             if data['response']['docs'] == []:
                 logging.warning("No Data fetched about the gene {}!".format(hgnc_symbol))
                 #sys.exit()
             else:
                 logging.info("Data for the gene symbol {} retrieved".format(hgnc_symbol))
                 with open(os.path.join(startup.data_path,hgnc_symbol+'.json'),"w") as f:
                     json.dump(data,f)
                     logging.info("The data about the gene {} is written in the file {}.json.".format(hgnc_symbol,hgnc_symbol))
        elif response['status'] != '200':
            logging.error("Data cannot be Retrieved and the status code is {}!".format(response['status']))
    return data , uri+path



def extracting_identifiers(hgnc_symbol):
    identifier = {}
    data_from_api, link = downloading_from_API(hgnc_symbol)

#data_from_api['response']['docs'][0]['hgnc_id'] if present else None using get method
    if data_from_api['response']['numFound']==1 :
        identifier[hgnc_symbol] = ((data_from_api['response']['docs'][0]).get("hgnc_id","None"),
                                  (data_from_api['response'] ['docs'][0]).get("ensembl_gene_id","None"),
                                  (data_from_api['response'] ['docs'][0]).get("uniprot_ids","None"))
        return identifier,link
    else:
        return None


#print(extracting_identifiers("CREBBP"))

# start of the Click
@click.group()
def main():
    pass
@main.command()
@click.option('-hgnc','--hgnc_symbol',help='Name of the HGNC symbol')

def info (hgnc_symbol=None) -> None:
      print(extracting_identifiers(hgnc_symbol))

if __name__ == '__main__':
    main()


# fulll correct