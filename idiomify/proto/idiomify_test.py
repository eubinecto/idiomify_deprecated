from gensim.models import Word2Vec
from idiomify.paths import NLP_MODEL, IDIOM2VEC_WV_001_BIN, IDIOM2VEC_WV_002_BIN
from idiomify.idiomifiers import Word2VecIdiomifier
from identify_idioms.service import load_idioms
from spacy import load


def main():
    # --- prepare the models --- #
    nlp = load(NLP_MODEL)
    idiom2vec_1 = Word2Vec.load(IDIOM2VEC_WV_001_BIN)
    idiom2vec_2 = Word2Vec.load(IDIOM2VEC_WV_002_BIN)
    idiom_keys_1 = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        if idiom2vec_1.wv.key_to_index.get(idiom.replace(" ", "_"), None)
    ]
    idiom_keys_2 = [
        idiom.replace(" ", "_")
        for idiom in load_idioms()
        if idiom2vec_2.wv.key_to_index.get(idiom.replace(" ", "_"), None)
    ]
    print(idiom_keys_2)
    # --- instantiate idiomifiers --- #
    idiomifier_001 = Word2VecIdiomifier(nlp, idiom_keys_1, idiom2vec_1)
    idiomifier_002 = Word2VecIdiomifier(nlp, idiom_keys_2, idiom2vec_2)

    print("---- with word2vec ----")
    phrase = "feeling nervous"
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_001(phrase)[: 10]:
        print(idiom, score)
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_002(phrase)[: 10]:
        print(idiom, score)
    phrase = "An intentional obliviousness."
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_001(phrase)[: 10]:
        print(idiom, score)
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_002(phrase)[: 10]:
        print(idiom, score)
    phrase = "cause something to fail or go wrong"
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_001(phrase)[: 10]:
        print(idiom, score)
    print("### {} ###".format(phrase))
    for idiom, score in idiomifier_002(phrase)[: 10]:
        print(idiom, score)


if __name__ == '__main__':
    main()
