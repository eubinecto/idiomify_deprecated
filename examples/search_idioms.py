from gensim.models import Word2Vec
from idiomify.paths import IDIOM2VEC_MODEL, TARGET_IDIOMS_TXT
from idiomify.loaders import TargetIdiomsLoader


def main():
    idiom2vec = Word2Vec.load(str(IDIOM2VEC_MODEL))
    target_idioms = TargetIdiomsLoader().load(TARGET_IDIOMS_TXT, norm=True)
    idiom_indices = [
        idiom2vec.wv.key_to_index.get(idiom, None)
        for idiom in target_idioms
    ]
    print(idiom_indices)
    idiom2vec.wv.most_similar_to_given()


if __name__ == '__main__':
    main()
