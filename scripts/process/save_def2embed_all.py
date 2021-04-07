"""
just build (def=input, embedding=target, idiom) pair for each idiom.
"""
import csv
import json
from idiomify.loaders import load_defs, load_target_embeds, load_target_idioms
from idiomify.paths import DEF2EMBED_ALL_TSV


def main():
    # load the definitions, in dict
    merged_defs = dict(load_defs('merged'))
    # load the embeddings, in dict
    target_embeds = dict(load_target_embeds())
    # load the target idioms
    target_idioms = load_target_idioms()

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
