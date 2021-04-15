"""
just build (def=input, embedding=target, idiom) pair for each idiom.
"""
import csv
import json

from gensim.models import Word2Vec, KeyedVectors
from identify_idioms.service import load_idioms
from idiomify.loaders import TargetIdiomsLoader, TsvTuplesLoader
from idiomify.paths import (
    MERGED_DEFS_TSV,
    TARGET_EMBEDDINGS_TSV,
    DEF2EMBED_ALL_TSV,
    TARGET_IDIOMS_TXT,
    IDIONLY2VEC_KV
)


def main():
    # load the definitions, in dict
    tsv_tuples_loader = TsvTuplesLoader()
    idionly2vec = KeyedVectors.load_word2vec_format(IDIONLY2VEC_KV)
    merged_defs = dict(tsv_tuples_loader.load(MERGED_DEFS_TSV))
    # load the embeddings, in dict
    # load the target idioms
    idioms = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
    ]

    with open(DEF2EMBED_ALL_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom in idioms:
            if idiom == "beat_around_the_bush":
                print("SKIP:" + idiom)
                continue
            if not idionly2vec.key_to_index.get(idiom, None):
                print("SKIP:" + idiom)
                continue
            defs = merged_defs[idiom]
            embed = idionly2vec.get_vector(idiom)
            for idiom_def in defs:
                to_write = [idiom_def, json.dumps(embed.tolist())]
                tsv_writer.writerow(to_write)


if __name__ == '__main__':
    main()
