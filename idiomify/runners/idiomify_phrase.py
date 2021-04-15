from gensim.models import Word2Vec, Doc2Vec
from idiomify.paths import NLP_MODEL, IDIOM2VEC_WV_001_BIN, IDIOM2VEC_DV_001_BIN
from idiomify.idiomifiers import Word2VecIdiomifier, Doc2VecIdiomifier
from identify_idioms.service import load_idioms
from spacy import load


def main():
    # --- prepare the models --- #
    nlp = load(NLP_MODEL)
    idiom2vec_wv = Word2Vec.load(IDIOM2VEC_WV_001_BIN)
    idiom2vec_dv = Doc2Vec.load(IDIOM2VEC_DV_001_BIN)  # doesn't really work..?
    idiom_keys = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        if idiom2vec_wv.wv.key_to_index.get(idiom, None)
        if idiom2vec_dv.wv.key_to_index.get(idiom, None)
    ]
    # --- instantiate idiomifiers --- #
    idiomifier_wv = Word2VecIdiomifier(nlp, idiom_keys, idiom2vec_wv)
    idiomifier_dv = Doc2VecIdiomifier(nlp, idiom_keys, idiom2vec_dv)

    print("---- with word2vec ----")
    phrase = "feeling nervous"
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_wv(phrase)[: 10]:
        print(idiom, score)

    phrase = "a dilemma or difficult circumstance"
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_wv(phrase)[: 10]:
        print(idiom, score)

    print("---- with doc2vec ---")
    phrase = "feeling nervous"
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_dv(phrase)[: 10]:
        print(idiom, score)

    phrase = "a dilemma or difficult circumstance"
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_dv(phrase)[: 10]:
        print(idiom, score)


if __name__ == '__main__':
    main()
