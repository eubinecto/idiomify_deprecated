"""
use rapid API to get definitions from urban dictionary.
in : list of (idiom, alts)
out list of (idiom, raws)
"""
from idiomify.paths import URBAN_IDIOM_RAWS_TSV
from typing import List, Tuple
from requests import HTTPError
from idiomify.loaders import load_idiom_alts, load_rapid_api_key
import requests
import csv
from multiprocessing import Pool

RAPID_API_KEY = load_rapid_api_key()
# the endpoint of rapid api
URL = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
# key and host
HEADERS = {
    'x-rapidapi-key': RAPID_API_KEY,
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
}


def to_raws(idiom_alts: Tuple[str, List[str]]) -> Tuple[str, list]:
    global RAPID_API_KEY, URL, HEADERS
    raws = list()
    idiom = idiom_alts[0]
    alts = idiom_alts[1]
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
    print("done:", idiom)
    return idiom, raws


def main():
    # the data to scrape (idiom -> raws)
    idiom_alts = load_idiom_alts()
    with Pool(processes=4) as p:
        idiom_raws = p.map(to_raws, idiom_alts)
    # now write them
    with open(URBAN_IDIOM_RAWS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raws in idiom_raws:
            tsv_writer.writerow([idiom, raws])


if __name__ == '__main__':
    main()
