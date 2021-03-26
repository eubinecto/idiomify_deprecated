from typing import List, Dict
from idiomify.paths import IDIOM_ALTS_TSV
import csv
import json


def load_idiom_alts() -> Dict[str, List[str]]:
    rows = dict()
    with open(IDIOM_ALTS_TSV, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        # skip the header
        next(tsv_reader)
        for row in tsv_reader:
            idiom = row[0]
            alts = json.loads(row[1])
            rows[idiom] = alts

    return rows
