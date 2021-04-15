"""
Will experiment with different models.
"""
from typing import List, Tuple
from gensim.models import Word2Vec, Doc2Vec
from spacy import Language


class Idiomifier:
    def __init__(self, nlp: Language, idiom_keys: List[str]):
        self.nlp = nlp
        self.idiom_keys = idiom_keys  # make sure they are available keys.

    def __call__(self, phrase: str) -> List[Tuple[str, float]]:
        raise NotImplementedError

    def to_tokens(self, phrase: str) -> List[str]:
        # refine the phrase
        return [
            token.lemma_  # lemmatise it
            for token in self.nlp(phrase)
            if not token.is_stop
            if not token.is_punct
            if not token.like_num
        ]


class Doc2VecIdiomifier(Idiomifier):
    """
    use infer_vector method to get the vector representation as a whole!
    """

    def __init__(self, nlp: Language, idiom_keys: List[str], idiom2vec_dv: Doc2Vec):
        super().__init__(nlp, idiom_keys)
        self.idiom2vec_dv = idiom2vec_dv

    def __call__(self, phrase: str) -> List[Tuple[str, float]]:
        tokens = self.to_tokens(phrase)
        phrase_vector = self.idiom2vec_dv.infer_vector(tokens)  # use value from model init
        sim_to_idioms = self.idiom2vec_dv.wv.distances(phrase_vector, self.idiom_keys)
        sims = list(zip(self.idiom_keys, sim_to_idioms))
        return sorted(sims, key=lambda x: x[1], reverse=True)


class Word2VecIdiomifier(Idiomifier):
    """
    make sure you do this with tfidf model.
    """
    def __init__(self, nlp: Language, idiom_keys: List[str], idiom2vec_wv: Word2Vec):
        super().__init__(nlp, idiom_keys)
        self.idiom2vec_wv = idiom2vec_wv

    def __call__(self, phrase: str) -> List[Tuple[str, float]]:
        """
        idiomify the phrase with a pretrained word2vec.
        :param phrase:
        :return: a list of tuples. [idiom, score]
        """
        tokens = self.to_tokens(phrase)
        # correlations between the sets.
        sim_to_idioms = [
            self.idiom2vec_wv.wv.n_similarity(tokens, [idiom_key])
            for idiom_key in self.idiom_keys
        ]
        sims = list(zip(self.idiom_keys, sim_to_idioms))
        return sorted(sims, key=lambda x: x[1], reverse=True)
