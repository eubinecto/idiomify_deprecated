import csv
import json
from typing import Tuple
import requests
from requests import HTTPError
from idiomify.paths import WORDNIK_RAWS_TSV
from idiomify.loaders import load_key, load_target_idioms

URL = "https://api.wordnik.com/v4/word.json/{word}/definitions"

PARAMS = {
        'api_key': load_key('wordnik'),
        'limit': 200,
        'sourceDictionaries': 'all',
        'useCanonical': True
    }


def to_raws(idiom: str) -> Tuple[str, list]:
    global URL, PARAMS
    request_url = URL.format(word=idiom)
    r = requests.get(request_url, params=PARAMS)
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
    idiom_raws = [
        to_raws(idiom)
        for idiom in target_idioms
    ]

    # now write them
    with open(WORDNIK_RAWS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raws in idiom_raws:
            tsv_writer.writerow([idiom, json.dumps(raws)])


if __name__ == '__main__':
    main()
