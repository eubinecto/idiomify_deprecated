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

    def refine(self, phrase: str) -> List[Tuple[str, str]]:
        return [
            (token.lemma_.lower())  # lemmatise and uncase
            for token in self.nlp(phrase)
            if not token.is_punct  # filter punctuations.
            if not token.like_num  # filter numbers.
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
        # 1. get the phrase vector
        phrase_vector = self.phrase_vector(phrase, mode)
        # 2. and find the most similar idioms.
        return self.most_similar_idioms(phrase_vector)

    def phrase_vector(self, phrase: str, mode: str) -> np.array:
        # 1. lemmatise the phrase
        tokens = self.refine(phrase)
        # 2. get the tokens that the idiom2vec has seen in the training
        avail_tokens = [
            token
            for token in tokens
            if self.idiom2vec_wv.wv.key_to_index.get(token, None)
        ]
        # 3. vectorize the tokens.
        token_vectors = [
            self.idiom2vec_wv.wv.get_vector(token)
            for token in avail_tokens
        ]
        # 4. abort if Idiom2Vec has not seen any of the tokens in training
        if len(token_vectors) == 0:
            # a placeholder
            print("no tokens")
            return None
        # 5. average the token vectors to get the phrase vector and return
        return np.array(token_vectors).mean(axis=0)

    def most_similar_idioms(self, vector: np.array) -> List[Tuple[str, float]]:
        sim_to_idioms = self.idiom2vec_wv.wv.cosine_similarities(vector, self.idiom_vectors)
        sims = list(zip(self.idiom_keys, sim_to_idioms))
        return sorted(sims, key=lambda x: x[1], reverse=True)
