from typing import List, Tuple

import numpy as np
from gensim.models import Word2Vec
from identify_idioms.service import load_idioms
from idiom2collocations.loaders import load_lemma2idfs
from spacy import load
from idiomify.idiomifiers import Word2VecIdiomifier
from idiomify.loaders import load_idiom2def
from idiomify.paths import IDIOM2VEC_WV_002_BIN, NLP_MODEL, IDIOM2VEC_WV_001_BIN, IDIOM2VEC_WV_003_BIN
from matplotlib import pyplot as plt


def get_mrr(idiomifier: Word2VecIdiomifier,
            idiom2def: List[Tuple[str, str]],
            phrase_vector_mode: str) -> float:
    """
    compute mean reciprocal rate.
    :param idiomifier:
    :param idiom2def:
    :param phrase_vector_mode:
    :return:
    """
    ranks = list()
    for idiom, def_ in idiom2def:
        # error handling goes here.
        if not idiomifier.idiom2vec_wv.wv.key_to_index.get(idiom, None):
            continue
        if idiomifier.phrase_vector(def_, 'avg') is None:
            continue
        docs = [
            idiom
            for idiom, _ in idiomifier(def_, phrase_vector_mode)
        ]
        # get the rank
        rank = docs.index(idiom) + 1
        ranks.append(rank)
    ranks_reciprocal = [
        1 / rank
        for rank in ranks
    ]
    # the mrr formula.
    return sum(ranks_reciprocal) / len(ranks_reciprocal)


def plot_mrrs(mrr_a: float,
              mrr_b: float,
              mrr_c: float,
              mrr_d: float,
              mrr_e: float):
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([mrr_a, mrr_b, mrr_c, mrr_d, mrr_e])
    # Calculate the simple average of the data
    y_mean = [np.mean(y)] * len(x)
    x_ticks = ["A(1-2)", "B(77-78)", "C(195-199)", "D(555-567)", "E(23115-142905)"]
    plt.xticks(x, x_ticks)
    plt.bar(x, y)
    plt.xlabel("The frequency groups")
    plt.title("MRR over different frequency groups")
    plt.ylabel("MRR")
    plt.plot(x, y_mean, label='mean', linestyle='--', color='k')
    plt.legend(loc='upper right')
    plt.show()


def main():
    idiom2def = load_idiom2def()
    idiom2vec = Word2Vec.load(IDIOM2VEC_WV_002_BIN)
    # --- nlp model to tokenise a given phrase --- #
    nlp = load(NLP_MODEL)
    # -- get the keys --- #
    idiom_keys = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        # only if the model has seen the idiom.
        if idiom2vec.wv.key_to_index.get(idiom.replace(" ", "_"), None)
    ]
    # --- instantiate the idiomifiers --- #
    idiomifier = Word2VecIdiomifier(nlp, idiom_keys, idiom2vec)
    # get the mrr's
    mrr_a = get_mrr(idiomifier, list(idiom2def)[:20], "avg")
    mrr_b = get_mrr(idiomifier, list(idiom2def)[20:40], "avg")
    mrr_c = get_mrr(idiomifier, list(idiom2def)[40:60], "avg")
    mrr_d = get_mrr(idiomifier, list(idiom2def)[60:80], "avg")
    mrr_e = get_mrr(idiomifier, list(idiom2def)[80:100], "avg")
    plot_mrrs(mrr_a, mrr_b, mrr_c, mrr_d, mrr_e)

    # evaluate idiom2vec. on all of them.
    idiom2vec_001 = Word2Vec.load(IDIOM2VEC_WV_001_BIN)
    idiom2vec_002 = Word2Vec.load(IDIOM2VEC_WV_002_BIN)
    idiom2vec_003 = Word2Vec.load(IDIOM2VEC_WV_003_BIN)

    # -- get the keys --- #
    idiom_keys_1 = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        # only if the model has seen the idiom.
        if idiom2vec_001.wv.key_to_index.get(idiom.replace(" ", "_"), None)
    ]
    # -- get the keys --- #
    idiom_keys_2 = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        # only if the model has seen the idiom.
        if idiom2vec_002.wv.key_to_index.get(idiom.replace(" ", "_"), None)
    ]
    # -- get the keys --- #
    idiom_keys_3 = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        # only if the model has seen the idiom.
        if idiom2vec_003.wv.key_to_index.get(idiom.replace(" ", "_"), None)
    ]

    # --- instantiate the idiomifiers --- #
    idiomifier_1 = Word2VecIdiomifier(nlp, idiom_keys_1, idiom2vec_001)
    idiomifier_2 = Word2VecIdiomifier(nlp, idiom_keys_2, idiom2vec_002)
    idiomifier_3 = Word2VecIdiomifier(nlp, idiom_keys_3, idiom2vec_003)

    mrr_1 = get_mrr(idiomifier_1, list(idiom2def), "avg")
    mrr_2 = get_mrr(idiomifier_2, list(idiom2def), "avg")
    mrr_3 = get_mrr(idiomifier_3, list(idiom2def), "avg")

    print("----evaluating idiom2vecs----")
    print("v1: {}".format(mrr_1))
    print("v2: {}".format(mrr_2))
    print("v3: {}".format(mrr_3))


if __name__ == '__main__':
    main()
