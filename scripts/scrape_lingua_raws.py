"""
lingua api compiles the senses from Wiktionary.
"""
import csv
import json
from multiprocessing import Pool
from typing import Tuple
import requests
from requests import HTTPError
from idiomify.loaders import ApiKeyLoader, TargetIdiomsLoader
from idiomify.paths import (
    LINGUA_RAWS_TSV,
    RAPID_KEY_TXT,
    TARGET_IDIOMS_TXT
)


URL = "https://lingua-robot.p.rapidapi.com/language/v1/entries/en/"

HEADERS = {
    'x-rapidapi-key': ApiKeyLoader().load(RAPID_KEY_TXT),
    'x-rapidapi-host': "lingua-robot.p.rapidapi.com"
    }


def to_raws(idiom: str) -> Tuple[str, list]:
    global URL, HEADERS
    request_url = URL + idiom
    r = requests.get(request_url, headers=HEADERS)
    try:
        r.raise_for_status()
    except HTTPError as he:
        print("no definitions for:", idiom)
        print("error message:", str(he))
        raw = dict()
    else:
        raw = r.json()
    print("done:", idiom)
    return idiom, raw


def main():
    # the data to scrape (idiom -> raws)
    target_idioms = TargetIdiomsLoader().load(TARGET_IDIOMS_TXT)
    with Pool(processes=4) as p:
        idiom_raws = p.map(to_raws, target_idioms)
    # now write them
    with open(LINGUA_RAWS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raws in idiom_raws:
            tsv_writer.writerow([idiom, json.dumps(raws)])


if __name__ == '__main__':
    main()
