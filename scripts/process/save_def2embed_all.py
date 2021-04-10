"""
just build (def=input, embedding=target, idiom) pair for each idiom.
"""
import csv
import json
from idiomify.loaders import TargetIdiomsLoader, TsvTuplesLoader
from idiomify.paths import (
    MERGED_DEFS_TSV,
    TARGET_EMBEDDINGS_TSV,
    DEF2EMBED_ALL_TSV,
    TARGET_IDIOMS_TXT
)


def main():
    # load the definitions, in dict
    tsv_tuples_loader = TsvTuplesLoader()
    merged_defs = dict(tsv_tuples_loader.load(MERGED_DEFS_TSV))
    # load the embeddings, in dict
    target_embeds = dict(tsv_tuples_loader.load(TARGET_EMBEDDINGS_TSV))
    # load the target idioms
    target_idioms = TargetIdiomsLoader().load(TARGET_IDIOMS_TXT)

    with open(DEF2EMBED_ALL_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom in target_idioms:
            defs = merged_defs[idiom]
            embed = target_embeds[idiom]
            if not embed:
                print("SKIP:" + idiom)
                continue
            for idiom_def in defs:
                to_write = [idiom_def, json.dumps(embed)]
                tsv_writer.writerow(to_write)


if __name__ == '__main__':
    main()
