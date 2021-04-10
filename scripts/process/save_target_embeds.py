import json

from gensim.models import Word2Vec
from idiomify.loaders import TargetIdiomsLoader
from idiomify.paths import IDIOM2VEC_MODEL, TARGET_EMBEDDINGS_TSV, TARGET_IDIOMS_TXT
import logging
import csv
from sys import stdout
logging.basicConfig(stream=stdout, level=logging.INFO)


def main():
    # load idiom2vec
    idiom2vec_model = Word2Vec.load(str(IDIOM2VEC_MODEL))
    # load the target idioms
    target_idioms_loader = TargetIdiomsLoader()
    target_idioms = target_idioms_loader.load(TARGET_IDIOMS_TXT)
    target_idioms_norm = target_idioms_loader.load(TARGET_IDIOMS_TXT, norm=True)
    # idiom ...?
    with open(TARGET_EMBEDDINGS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, idiom_norm in zip(target_idioms, target_idioms_norm):
            try:
                # transform it into a list
                idiom_vec = idiom2vec_model.wv.get_vector(idiom_norm).tolist()
            except KeyError:
                idiom_vec = None
            finally:
                to_write = [idiom, json.dumps(idiom_vec)]
                tsv_writer.writerow(to_write)


if __name__ == '__main__':
    main()
