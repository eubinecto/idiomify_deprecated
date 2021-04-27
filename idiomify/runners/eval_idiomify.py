from typing import List, Tuple

import numpy as np
from gensim.models import Word2Vec
from identify_idioms.service import load_idioms
from idiom2collocations.loaders import load_lemma2idfs
from spacy import load
from idiomify.idiomifiers import Word2VecIdiomifier
from idiomify.loaders import load_idiom2syns
from idiomify.paths import IDIOM2VEC_WV_002_BIN, NLP_MODEL, IDIOM2VEC_WV_001_BIN, IDIOM2VEC_WV_003_BIN
from matplotlib import pyplot as plt


def get_ranks(idiomifier: Word2VecIdiomifier, idiom2def: List[Tuple[str, str]], phrase_vector_mode: str):
    ranks = list()
    for idiom, def_ in idiom2def:
        if not idiomifier.idiom2vec_wv.wv.key_to_index.get(idiom, None):
            continue
        if idiomifier.phrase_vector(def_, 'avg') is None:
            continue
        # the bigger the score, the better it is. (dot product)
        idioms_ranked = [
            idiom
            for idiom, _ in idiomifier(def_, phrase_vector_mode)
        ]
        # get the rank
        rank = idioms_ranked.index(idiom) + 1
        ranks.append(rank)
    return ranks


def plot_ranks(ranks: List[float], title: str):
    x = np.array([0, 1, 2, 3, 4])
    ranks_a = ranks[:10]
    ranks_b = ranks[10:20]
    ranks_c = ranks[20:30]
    ranks_d = ranks[30:40]
    ranks_e = ranks[40:50]
    y = np.array([sum(ranks_a) / 10,
                  sum(ranks_b) / 10,
                  sum(ranks_c) / 10,
                  sum(ranks_d) / 10,
                  sum(ranks_e) / 10])
    x_ticks = ["A(1-2)", "B(77-78)", "C(195-199)", "D(555-567)", "E(23115-142905)"]
    plt.xticks(x, x_ticks)
    plt.bar(x, y)
    plt.xlabel("The frequency groups")
    plt.title(title)
    plt.ylabel("Average ranks")
    plt.show()


def main():
    idiom2def = load_idiom2syns()
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

    # get the idfs
    lemma2idfs = list(load_lemma2idfs())
    verb2idf = dict(map(lambda x: (x[0], x[1]), lemma2idfs))
    noun2idf = dict(map(lambda x: (x[0], x[2]), lemma2idfs))
    adj2idf = dict(map(lambda x: (x[0], x[3]), lemma2idfs))
    adv2idf = dict(map(lambda x: (x[0], x[4]), lemma2idfs))
    idfs = (verb2idf, noun2idf, adj2idf, adv2idf)
    # --- instantiate the idiomifiers --- #
    idiomifier = Word2VecIdiomifier(nlp, idiom_keys, idiom2vec, idfs)

    ranks = get_ranks(idiomifier, list(idiom2def), "avg")

    plot_ranks(ranks, title="The average of the target idiom ranks with the four frequency groups")

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

    # get the idfs
    lemma2idfs = list(load_lemma2idfs())
    verb2idf = dict(map(lambda x: (x[0], x[1]), lemma2idfs))
    noun2idf = dict(map(lambda x: (x[0], x[2]), lemma2idfs))
    adj2idf = dict(map(lambda x: (x[0], x[3]), lemma2idfs))
    adv2idf = dict(map(lambda x: (x[0], x[4]), lemma2idfs))
    idfs = (verb2idf, noun2idf, adj2idf, adv2idf)

    # --- instantiate the idiomifiers --- #
    idiomifier_1 = Word2VecIdiomifier(nlp, idiom_keys_1, idiom2vec_001, idfs)
    idiomifier_2 = Word2VecIdiomifier(nlp, idiom_keys_2, idiom2vec_002, idfs)
    idiomifier_3 = Word2VecIdiomifier(nlp, idiom_keys_3, idiom2vec_003, idfs)

    ranks_1 = get_ranks(idiomifier_1, list(idiom2def), "avg")
    ranks_2 = get_ranks(idiomifier_2, list(idiom2def), "avg")
    ranks_3 = get_ranks(idiomifier_3, list(idiom2def), "avg")

    print("----evaluating idiom2vecs----")
    print(sum(ranks_1) / len(ranks_1))
    print(sum(ranks_2) / len(ranks_2))
    print(sum(ranks_3) / len(ranks_3))

    print("---evaluating with svd vs. without svd---")
    # TODO: Do this later on.


if __name__ == '__main__':
    main()
