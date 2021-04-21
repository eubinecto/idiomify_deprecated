"""
idiomify a phrase here.
10-most closest idioms will be shown here, with colors.
"""
import argparse
from typing import List, Tuple
from tabulate import tabulate
from termcolor import colored
from gensim.models import Word2Vec
from identify_idioms.service import load_idioms
from spacy import load
from idiomify.idiomifiers import Word2VecIdiomifier
from idiomify.paths import IDIOM2VEC_WV_001_BIN, IDIOM2VEC_WV_002_BIN, NLP_MODEL
from idiom2collocations.loaders import load_idiom2colls, load_lemma2idfs
import logging
from sys import stdout
logging.basicConfig(stream=stdout, level=logging.ERROR)


def display_results(phrase: str, results: List[Tuple[str, float]], colls_mode: str):
    print("### idiomifying: {}, colls mode: {} ###".format(phrase, colls_mode))
    # --- load collocations --- #
    idiom2colls = dict(load_idiom2colls(colls_mode).map(lambda x: (x[0], x[1:])))
    table = list()
    for idiom, score in results:
        colls = idiom2colls.get(idiom, None)
        row = [
            idiom,
            str(score)
        ]
        if colls:
            row += [
                colored(str(idiom2colls[idiom][0][:5]), color='yellow'),
                colored(str(idiom2colls[idiom][1][:5]), color='blue'),
                colored(str(idiom2colls[idiom][2][:5]), color='magenta'),
                colored(str(idiom2colls[idiom][3][:5]), color='cyan')
            ]
        else:
            row += []*4
        table.append(row)
    print(tabulate(table, headers=['idiom', 'score', 'verb collocates', 'noun collocates',
                                   'adj collocates', 'adv collocates']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phrase",
                        type=str,
                        default="a dilemma or a difficult situation")
    parser.add_argument("--phrase_vector_mode",
                        type=str,
                        default="avg")
    parser.add_argument("--idiom2vec_ver",
                        type=str,
                        default="002")
    parser.add_argument("--colls_mode",
                        type=str,
                        default="pmi")
    parser.add_argument("--top_n",
                        type=int,
                        default=10)
    args = parser.parse_args()
    # --- get idiom2vec --- #
    if args.idiom2vec_ver == "001":
        idiom2vec = Word2Vec.load(IDIOM2VEC_WV_001_BIN)
    elif args.idiom2vec_ver == "002":
        idiom2vec = Word2Vec.load(IDIOM2VEC_WV_002_BIN)
    else:
        raise ValueError

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

    # --- instantiate a idiomifier --- #
    idiomifier = Word2VecIdiomifier(nlp, idiom_keys, idiom2vec, idfs)

    # --- idiomify the phrase --- #
    results = idiomifier(args.phrase, mode=args.phrase_vector_mode)[:args.top_n]

    # --- show the result --- #
    display_results(args.phrase, results, args.colls_mode)


if __name__ == '__main__':
    main()
