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


def evaluate(idiomifier: Word2VecIdiomifier, idiom2syns: List[Tuple[str, str]], phrase_vector_mode: str):
    scores = list()
    for idiom, syns in idiom2syns:
        # the bigger the score, the better it is. (dot product)
        idiom2score = dict(idiomifier(syns, phrase_vector_mode))
        score = idiom2score.get(idiom, 0)
        print(idiom, score)
        scores.append(score)
    return scores


def plot_scores(scores: List[float], title: str):
    x = np.array([0, 1, 2, 3])
    y = np.array([sum(scores[9:12]) / 3, sum(scores[6:9]) / 3, sum(scores[3:6]) / 3, sum(scores[:3]) / 3])
    x_ticks = ["A (1)", "B (64)", "C (1178)", "D (74866)"]
    plt.xticks(x, x_ticks)
    plt.bar(x, y)
    plt.xlabel("Average frequency of the group")
    plt.ylim(0, 1)
    plt.title(title)
    plt.ylabel("Average of the target idiom score (avg of dot products)")
    plt.show()


def plot_idiom2vec_eval(avg_score_1: float, avg_score_2: float, avg_score_3: float):
    x = np.array([0, 1, 2])
    y = np.array([avg_score_1, avg_score_2, avg_score_3])
    x_ticks = ["V1", "V2", "V3"]
    plt.xticks(x, x_ticks)
    plt.bar(x, y)
    plt.xlabel("Idiom2Vecs in different versions")
    plt.ylim(0, 1)
    plt.title("The average of the target scores with different versions of Idiom2Vec")
    plt.ylabel("Average of the target idiom score (avg of dot products)")
    plt.show()


def main():
    idiom2syns = load_idiom2syns()
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

    scores = evaluate(idiomifier, list(idiom2syns), "avg")

    print(list(idiom2syns))

    frequent_scores = scores[: 3]
    avg_scores = scores[3: 6]
    low_scores = scores[6: 9]
    very_low_scores = scores[9: 12]

    print("{} / {}".format(sum(frequent_scores), 3))
    print("{} / {}".format(sum(avg_scores), 3))
    print("{} / {}".format(sum(low_scores), 3))
    print("{} / {}".format(sum(very_low_scores), 3))

    plot_scores(scores, title="The average of the target idiom scores with the four frequency groups")

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

    scores_1 = evaluate(idiomifier_1, list(idiom2syns), "avg")
    scores_2 = evaluate(idiomifier_2, list(idiom2syns), "avg")
    scores_3 = evaluate(idiomifier_3, list(idiom2syns), "avg")

    print(sum(scores_1) / len(scores_1))
    print(sum(scores_2) / len(scores_2))
    print(sum(scores_3) / len(scores_3))
    plot_idiom2vec_eval(sum(scores_1) / len(scores_1),
                        sum(scores_2) / len(scores_2),
                        sum(scores_3) / len(scores_3))


if __name__ == '__main__':
    main()
