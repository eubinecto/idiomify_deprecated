import csv
import json
from itertools import cycle
from typing import Tuple
from idiomify.loaders import load_target_idioms
from idiomify.scrapers import ThefreeRawsScraper
from idiomify.paths import THEFREE_RAWS_TSV
import time
from tqdm import tqdm

# so that I don't get caught
PROXIES = [
    'http://64.225.26.142:8080',  # US
    'http://124.48.218.245:80',
    'http://116.73.14.16:8080',
    'http://51.75.144.32:3128'
]


# use this
proxy_pool = cycle(PROXIES)


def to_raws(idiom: str) -> Tuple[str, list]:
    proxy = next(proxy_pool)
    raws = ThefreeRawsScraper.fetch(idiom, proxy)
    print((idiom, raws))
    return idiom, raws


def main():
    target_idioms = load_target_idioms()
    # it seems hyphens don't help here.
    idiom_raws = list()
    for idiom in tqdm(target_idioms):
        time.sleep(0.2)
        idiom_raws.append(to_raws(idiom))

    with open(THEFREE_RAWS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raws in idiom_raws:
            tsv_writer.writerow([idiom, json.dumps(raws)])


if __name__ == '__main__':
    main()
