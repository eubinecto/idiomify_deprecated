import json

from idiomify.loaders import load_defs, load_target_idioms
from idiomify.paths import MERGED_DEFS_TSV
import csv


def main():
    # a list of tuples -> dict
    lingua_defs = dict(load_defs('lingua'))
    thefree_defs = dict(load_defs('thefree'))
    target_idioms = load_target_idioms()
    with open(MERGED_DEFS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom in target_idioms:
            defs = lingua_defs[idiom] + thefree_defs[idiom]
            tsv_writer.writerow([idiom, json.dumps(defs)])


if __name__ == '__main__':
    main()
