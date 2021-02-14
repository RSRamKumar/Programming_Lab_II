import os
import json
import logging
from typing import Optional

import requests

from .startup import DATA_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Profiler:
    """Creates a data profile for a given HGNC symbol based on information downloaded from HGNC."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.cache_file_path = os.path.join(DATA_DIR, f"{symbol.lower()}.json")
        self.raw_hgnc_data = None

    def cache_file_exists(self) -> bool:
        """Checks if cache file exists."""
        return True if os.path.exists(self.cache_file_path) else False

    def get_identifers(self) -> Optional[dict]:
        """Gathers HGNC ID, EnSembl Gene ID, and UniPRot IDs from raw HGNC data.

        Returns
        -------
        dict, None
            Returns identifiers as dict if data available, else None.
        """
        self.get_hgnc_data()
        identifiers = dict()
        if self.raw_hgnc_data:
            if len(self.raw_hgnc_data['docs']) > 1:
                logger.debug(f"{self.symbol} has more than 1 'docs'")
            content = self.raw_hgnc_data['docs'][0]
            identifiers['hgnc'] = content["hgnc_id"] if "hgnc_id" in content else None
            identifiers['ensembl'] = content["ensembl_gene_id"] if "ensembl_gene_id" in content else None
            identifiers['uniprot'] = content["uniprot_ids"] if "uniprot_ids" in content else None
            return identifiers

    def read_cache_file(self):
        """Reads a stored cache file."""
        with open(self.cache_file_path, 'r') as cachefile:
            content = json.load(cachefile)
        self.raw_hgnc_data = content

    def get_hgnc_data(self):
        """Retrieves the raw data for the given HGNC symbol either by reading from cached file or downloading it."""
        if self.cache_file_exists():
            self.read_cache_file()

        else:
            self.download_hgnc_info()
            if self.raw_hgnc_data:
                self.__write_hgnc_to_cache()

    def __write_hgnc_to_cache(self) -> None:
        """Writes HGNC data to JSON file in cache."""
        with open(self.cache_file_path, 'w') as cachefile:
            json.dump(self.raw_hgnc_data, cachefile, indent=2)
        logger.info(f"Cache file for {self.symbol} successfully written to {self.cache_file_path}")

    def download_hgnc_info(self):
        """Downloads data using HGNC API for a given HGNC symbol.

        Returns
        -------
        dict, None
            Sets hgnc_data attribute if downloaded, else returns None.
        """
        api_query = f"http://rest.genenames.org/fetch/symbol/{self.symbol}"
        r = requests.get(api_query, headers={"Accept": "application/json"})  # Want JSON

        if r.status_code != 200:
            logger.error(f"{api_query} returned bad status code: {r.status_code}")

        response = r.json()['response']  # Other key is responseHeader
        if response['numFound'] > 0:  # Found a result
            self.raw_hgnc_data = response

        else:
            logger.warning(f"No results found for {self.symbol}")
