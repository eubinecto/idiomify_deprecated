import json

from idiomify.loaders import TsvTuplesLoader, TargetIdiomsLoader
from idiomify.paths import (
    MERGED_DEFS_TSV,
    LINGUA_DEFS_TSV,
    THEFREE_DEFS_TSV,
    TARGET_IDIOMS_TXT
)
import csv


def main():
    # a list of tuples -> dict
    tuples_loader = TsvTuplesLoader()
    lingua_defs = dict(tuples_loader.load(LINGUA_DEFS_TSV))
    thefree_defs = dict(tuples_loader.load(THEFREE_DEFS_TSV))
    target_idioms = TargetIdiomsLoader().load(TARGET_IDIOMS_TXT)
    with open(MERGED_DEFS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom in target_idioms:
            defs = lingua_defs[idiom] + thefree_defs[idiom]
            tsv_writer.writerow([idiom, json.dumps(defs)])


if __name__ == '__main__':
    main()
