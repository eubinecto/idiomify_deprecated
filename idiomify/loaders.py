from typing import List, Dict, Tuple
from idiomify.paths import IDIOM_ALTS_TSV, RAPID_API_TXT
import csv
import json


def load_idiom_alts() -> List[Tuple[str, List[str]]]:
    rows = list()
    with open(IDIOM_ALTS_TSV, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        # skip the header
        next(tsv_reader)
        for row in tsv_reader:
            idiom = row[0]
            alts = json.loads(row[1])
            rows.append((idiom, alts))
    return rows


def load_rapid_api_key() -> str:
    with open(RAPID_API_TXT, 'r') as fh:
        return fh.read().strip()
