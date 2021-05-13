from typing import List, Tuple
import numpy as np
from gensim.models import Word2Vec
from identify_idioms.service import load_idioms
from spacy import load
from idiomify.idiomifiers import Word2VecIdiomifier
from idiomify.loaders import load_idiom2def
from idiomify.paths import IDIOM2VEC_WV_002_BIN, NLP_MODEL, IDIOM2VEC_WV_001_BIN, IDIOM2VEC_WV_003_BIN
from matplotlib import pyplot as plt


def get_ranks(idiomifier: Word2VecIdiomifier,
              idiom2def: List[Tuple[str, str]],
              phrase_vector_mode: str) -> List[int]:
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
    return ranks


def median_and_var(ranks: List[int]) -> Tuple[int, float]:
    """
    doing this because this is how that paper evaluates it.
    :param ranks:
    :return:
    """
    return np.median(ranks), np.var(ranks)


def plot_medians(ranks_a: List[int],
                 ranks_b: List[int],
                 ranks_c: List[int],
                 ranks_d: List[int],
                 ranks_e: List[int]):
    median_d, var_d = median_and_var(ranks_d)
    median_e, var_e = median_and_var(ranks_e)

    x = np.array([0, 1])
    y = np.array([median_d, median_e])
    # Calculate the simple average of the data
    x_ticks = ["D(555-567)", "E(23115-142905)"]
    plt.xticks(x, x_ticks)
    plt.bar(x, y, width=0.5)
    plt.xlabel("The frequency groups")
    plt.title("Median Ranks of groups D and E")
    plt.ylabel("Median Rank")
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
    ranks = get_ranks(idiomifier, list(idiom2def), 'avg')
    median, var = median_and_var(ranks)
    print(median, var)
    ranks_a = get_ranks(idiomifier, list(idiom2def)[:20], "avg")
    ranks_b = get_ranks(idiomifier, list(idiom2def)[20:40], "avg")
    ranks_c = get_ranks(idiomifier, list(idiom2def)[40:60], "avg")
    ranks_d = get_ranks(idiomifier, list(idiom2def)[60:80], "avg")
    ranks_e = get_ranks(idiomifier, list(idiom2def)[80:100], "avg")
    plot_medians(ranks_a, ranks_b, ranks_c, ranks_d, ranks_e)

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

    ranks_1 = get_ranks(idiomifier_1, list(idiom2def), "avg")
    median_1, _ = median_and_var(ranks_1)
    ranks_2 = get_ranks(idiomifier_2, list(idiom2def), "avg")
    median_2, _ = median_and_var(ranks_2)
    ranks_3 = get_ranks(idiomifier_3, list(idiom2def), "avg")
    median_3, _ = median_and_var(ranks_3)

    print("----evaluating idiom2vecs----")
    print("v1 median: {}".format(median_1))
    print("v2 median: {}".format(median_2))
    print("v3 median: {}".format(median_3))


if __name__ == '__main__':
    main()
