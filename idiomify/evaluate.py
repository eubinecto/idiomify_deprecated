"""
evaluate:
1. sum vs. avg vs. w_avg.
2. stopwords & PRON included vs. stopwords &  PRON removed
"""
from gensim.models import Word2Vec
from identify_idioms.service import load_idioms
from idiom2collocations.loaders import load_lemma2idfs
from spacy import load
from idiomify.idiomifiers import Word2VecIdiomifier
from idiomify.loaders import load_idiom2defs
import argparse
from idiomify.paths import IDIOM2VEC_WV_001_BIN, IDIOM2VEC_WV_002_BIN, NLP_MODEL, IDIOM2VEC_WV_003_BIN, \
    IDIOM2VEC_WV_004_BIN


def evaluate(idiomifier: Word2VecIdiomifier, idiom2def: dict, phrase_vector_mode: str):
    scores = list()
    for idiom, def1 in idiom2def.items():
        # the bigger the score, the better it is. (dot product)
        idiom2score = dict(idiomifier(def1, phrase_vector_mode))
        scores.append(idiom2score.get(idiom, 0))
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phrase_vector_mode",
                        type=str,
                        default="avg")
    parser.add_argument("--idiom2vec_ver",
                        type=str,
                        default="002")
    args = parser.parse_args()
    # --- prepare idiomifier --- #
    # --- get idiom2vec --- #
    idiom2vec_001 = Word2Vec.load(IDIOM2VEC_WV_001_BIN)
    idiom2vec_002 = Word2Vec.load(IDIOM2VEC_WV_002_BIN)
    idiom2vec_003 = Word2Vec.load(IDIOM2VEC_WV_003_BIN)
    idiom2vec_004 = Word2Vec.load(IDIOM2VEC_WV_004_BIN)

    # --- nlp model to tokenise a given phrase --- #
    nlp = load(NLP_MODEL)

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
    # -- get the keys --- #
    idiom_keys_4 = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        # only if the model has seen the idiom.
        if idiom2vec_004.wv.key_to_index.get(idiom.replace(" ", "_"), None)
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
    idiomifier_4 = Word2VecIdiomifier(nlp, idiom_keys_4, idiom2vec_004, idfs)

    testable_idiom2def = dict([
        (idiom, def1.replace('\xa0', " "))
        for idiom, def1, _ in load_idiom2defs()
        if def1
    ])
    scores_1 = evaluate(idiomifier_1, testable_idiom2def, args.phrase_vector_mode)
    scores_2 = evaluate(idiomifier_2, testable_idiom2def, args.phrase_vector_mode)
    scores_3 = evaluate(idiomifier_3, testable_idiom2def, args.phrase_vector_mode)
    scores_4 = evaluate(idiomifier_4, testable_idiom2def, args.phrase_vector_mode)

    print("1: {} / {}".format(sum(scores_1), len(scores_1)))
    print("2: {} / {}".format(sum(scores_2), len(scores_2)))
    print("3: {} / {}".format(sum(scores_3), len(scores_3)))
    print("4: {} / {}".format(sum(scores_4), len(scores_4)))


if __name__ == '__main__':
    main()
