"""
use rapid API to get definitions from urban dictionary.
"""
from idiomify.paths import URBAN_DEFS_RAW_TSV
from typing import Dict
from requests import HTTPError
from idiomify.loaders import load_idiom_alts
import requests
import csv
from tqdm import tqdm


def main():
    URL = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    HEADERS = {
        'x-rapidapi-key': "e9f1d1caf0msh07763bffc4a60c5p1856e3jsnd0485d82d71d",
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }
    urban_raws: Dict[str, list] = dict()
    for idiom, alts in tqdm(load_idiom_alts().items()):
        # just collect raw responses
        raws = list()
        queries = [idiom] + alts
        for query in queries:
            query_string = {'term': query}
            r = requests.get(URL, headers=HEADERS, params=query_string)
            try:
                r.raise_for_status()
            except HTTPError as he:
                print("no definitions for:", query)
                print("error message:", str(he))
                continue
            else:
                raws.append(r.json())
        urban_raws[idiom] = raws

    # now write them
    with open(URBAN_DEFS_RAW_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raws in urban_raws.items():
            tsv_writer.writerow([idiom, raws])


if __name__ == '__main__':
    main()
