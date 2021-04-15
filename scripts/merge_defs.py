import json

from idiomify.loaders import TsvTuplesLoader, TargetIdiomsLoader
from idiomify.paths import (
    MERGED_DEFS_TSV,
    LINGUA_DEFS_TSV,
    THEFREE_DEFS_TSV,
)
import csv
from identify_idioms.service import load_idioms


def norm_case(idiom: str) -> str:
    return idiom.lower() \
        .replace("i ", "I ") \
        .replace(" i ", " I ") \
        .replace("i'm", "I'm") \
        .replace("i'll", "I'll") \
        .replace("i\'d", "I'd")


def main():
    # a list of tuples -> dict
    tuples_loader = TsvTuplesLoader()
    lingua_defs = dict([
        (norm_case(idiom).replace(" ", "_"), defs)
        for idiom, defs in tuples_loader.load(LINGUA_DEFS_TSV)
        ]
    )
    thefree_defs = dict([
        (norm_case(idiom).replace(" ", "_"), defs)
        for idiom, defs in tuples_loader.load(THEFREE_DEFS_TSV)
        ]
    )
    target_idioms = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
    ]
    with open(MERGED_DEFS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom in target_idioms:
            if idiom == "beat_around_the_bush":
                # maybe I've added this in manually later
                continue
            defs = lingua_defs[idiom] + thefree_defs[idiom]
            tsv_writer.writerow([idiom, json.dumps(defs)])


if __name__ == '__main__':
    main()
