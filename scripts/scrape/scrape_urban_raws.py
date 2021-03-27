"""
use rapid API to get definitions from urban dictionary.
in : list of (idiom, alts)
out list of (idiom, raws)
"""
import json
from idiomify.paths import URBAN_RAWS_TSV
from typing import List, Tuple
from requests import HTTPError
from idiomify.loaders import load_target_idioms, load_key
import requests
import csv
from multiprocessing import Pool

RAPID_API_KEY = load_key('rapid')
# the endpoint of rapid api
URL = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
# key and host
HEADERS = {
    'x-rapidapi-key': RAPID_API_KEY,
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
}


def to_raws(idiom: str) -> Tuple[str, list]:
    global URL, HEADERS
    query_string = {'term': idiom}
    r = requests.get(URL, headers=HEADERS, params=query_string)
    try:
        r.raise_for_status()
    except HTTPError as he:
        print("no definitions for:", idiom)
        print("error message:", str(he))
        raw = list()
    else:
        raw = r.json()
    print("done:", idiom)
    return idiom, raw


def main():
    # the data to scrape (idiom -> raws)
    target_idioms = load_target_idioms()
    with Pool(processes=2) as p:
        idiom_raws = p.map(to_raws, target_idioms)
    # now write them
    with open(URBAN_RAWS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raws in idiom_raws:
            tsv_writer.writerow([idiom, json.dumps(raws)])


if __name__ == '__main__':
    main()
