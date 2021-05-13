"""
Will experiment with different models.
"""
from typing import List, Tuple
import numpy as np
from gensim.models import Word2Vec
from spacy import Language


class Idiomifier:
    def __init__(self, nlp: Language, idiom_keys: List[str]):
        self.nlp = nlp
        self.idiom_keys = idiom_keys  # make sure they are available keys.

    def __call__(self, phrase: str) -> List[Tuple[str, float]]:
        raise NotImplementedError

    def to_lemma2pos(self, phrase: str) -> List[Tuple[str, str]]:
        # refine the phrase
        return [
            # uncased
            (token.lemma_.lower(), token.pos_)  # lemmatise it
            for token in self.nlp(phrase)
            # if not token.is_stop  # removing stopwords harms the performance
            if not token.is_punct
            if not token.like_num
        ]


class Word2VecIdiomifier(Idiomifier):
    """
    make sure you do this with tfidf model.
    """
    def __init__(self, nlp: Language, idiom_keys: List[str], idiom2vec_wv: Word2Vec):
        super().__init__(nlp, idiom_keys)
        self.idiom2vec_wv = idiom2vec_wv
        self.idiom_vectors = [
            self.idiom2vec_wv.wv.get_vector(idiom_key)
            for idiom_key in self.idiom_keys
        ]

    def __call__(self, phrase: str, mode: str = "avg") -> List[Tuple[str, float]]:
        """
        idiomify the phrase with a pretrained word2vec.
        :param phrase:
        :return: a list of tuples. [idiom, score]
        """
        phrase_vector = self.phrase_vector(phrase, mode)
        return self.most_similar_idioms(phrase_vector)

    def phrase_vector(self, phrase: str, mode: str) -> np.array:
        lemma2pos = self.to_lemma2pos(phrase)
        avail_lemma2pos = [
            (lemma, pos)
            for lemma, pos in lemma2pos
            if self.idiom2vec_wv.wv.key_to_index.get(lemma, None)
        ]
        token_vectors = [
            self.idiom2vec_wv.wv.get_vector(lemma)
            for lemma, _ in avail_lemma2pos
        ]
        if len(token_vectors) == 0:
            # a placeholder
            print("no tokens")
            return None

        if mode == "add":
            return np.array(token_vectors).sum(axis=0)
        if mode == "mul":
            return np.array(token_vectors).prod(axis=0)
        elif mode == "avg":
            return np.array(token_vectors).mean(axis=0)
        else:
            raise ValueError

    def most_similar_idioms(self, vector: np.array) -> List[Tuple[str, float]]:
        sim_to_idioms = self.idiom2vec_wv.wv.cosine_similarities(vector, self.idiom_vectors)
        sims = list(zip(self.idiom_keys, sim_to_idioms))
        return sorted(sims, key=lambda x: x[1], reverse=True)
