"""
Will experiment with different models.
Starting Lstm as the baseline. - this is mainly for learning experience.
Compare that with Bert. - should be better than lstm.
Compare that with SBert. - should be better than Bert.
Compare that with SBertEnhanced. (extracting pos representations). - should be better than SBert alone.
"""
from typing import List, Tuple

import torch
from gensim.models import Word2Vec
from transformers import BertModel, BertTokenizer


class Idiomifier(torch.nn.Module):

    def idiomify(self, phrase: str, idiom2vec: Word2Vec):
        """
        This is the target function to implement, basically.
        :return:
        """
        raise NotImplementedError


class LstmIdiomifier(Idiomifier):
    """
    uses LSTM for encoding a sentence.
    This is a baseline model.
    Learning to Understand Phrases by Embedding the Dictionary
    https://www.aclweb.org/anthology/Q16-1002/
    """

    def idiomify(self, phrase: str, idiom2vec: Word2Vec):
        pass


class BertIdiomifier(Idiomifier):
    """
    try this with Sentence BERT for encoding a sentence.
    https://arxiv.org/abs/1908.10084
    """
    def __init__(self, bert_model: BertModel, bert_tokenizer: BertTokenizer,
                 bert_embed_size: int, idiom2vec_embed_size: int, idioms: List[str]):
        """
        :param bert_model: (pretrained) bert model to be used for encoding a phrase (sentence)
        :param bert_tokenizer: the tokenizer that was used to train bert_model.
        :param idiom2vec_embed_size: should be the same as the output of idiom2vec model.
        """
        super().__init__()
        self.bert_model = bert_model
        self.bert_tokenizer = bert_tokenizer
        self.bert_embed_size = bert_embed_size
        self.idiom2vec_embed_size = idiom2vec_embed_size
        self.idioms = idioms
        self.linear = torch.nn.Linear(bert_embed_size, idiom2vec_embed_size)  # projection layer.

    def forward(self, phrases: List[str]) -> torch.Tensor:
        """
        :param phrases: list of phrases to encode. (1, N).
        :return:
        """
        # first, encode the sentence into token_ids, token_type_ids and attention masks.
        batch = self.bert_tokenizer(phrases,
                                    # return as pytorch tensor
                                    return_tensors='pt',
                                    # pad the short ones to have a batch of the same length
                                    padding=True)  # (N,M), where M = maximum length.
        # forward pass
        out = self.bert_model(**batch)  # idx = 0: token_hidden, 1: cls_hidden
        cls_hidden = out[1]  # (N, bert_embed_size)
        # down-project this with a linear layer and return
        return self.linear.forward(cls_hidden)  # (N, idiom2vec_embed_size)

    # this is for inference.
    def idiomify(self, phrase: str, idiom2vec: Word2Vec) -> List[Tuple[str, float]]:
        """
        given a query, this returns a
        :param phrase:
        :param idiom2vec:
        :return:
        """
        # get the prediction.
        phrase_vector = self.forward([phrase])
        # phrase similar by vector.
        sim_idioms = [
            (word, score)
            for word, score in idiom2vec.wv.similar_by_vector(vector=phrase_vector.numpy(), topn=None)
            if word in self.idioms  # only get those that are idioms.
        ]
        return sim_idioms


