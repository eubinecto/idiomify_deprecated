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

    def idiomify(self, phrase: str, bert_tokenizer: BertTokenizer, idiom2vec: Word2Vec) -> List[Tuple[str, float]]:
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

    def idiomify(self, phrase: str, bert_tokenizer: BertTokenizer, idiom2vec: Word2Vec) -> List[Tuple[str, float]]:
        pass


class BertIdiomifier(Idiomifier):
    """
    try this with Sentence BERT for encoding a sentence.
    https://arxiv.org/abs/1908.10084
    """
    def __init__(self, bert_model: BertModel,
                 bert_embed_size: int, idiom2vec_embed_size: int, idioms: List[str]):
        """
        :param bert_model: (pretrained) bert model to be used for encoding a phrase (sentence)
        :param idiom2vec_embed_size: should be the same as the output of idiom2vec model.
        """
        super().__init__()
        self.bert_model = bert_model
        self.bert_embed_size = bert_embed_size
        self.idiom2vec_embed_size = idiom2vec_embed_size
        self.idioms = idioms
        # projection layer.
        self.linear = torch.nn.Linear(bert_embed_size, idiom2vec_embed_size)

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        """
        :param X: (N, 3, M). 3 dimensional tensor. column 0: token ids, column 1: token type, column 3: pos encoding.
        :return:
        """
        X_token_ids = X[:, 0]
        X_token_type_ids = X[:, 1]
        X_attention_masks = X[:, 2]
        # forward pass of the bert model
        outs = self.bert_model(input_ids=X_token_ids,
                               attention_masks=X_attention_masks,
                               token_type_ids=X_token_type_ids)
        # idx = 0: token_hidden, 1: cls_hidden
        Y1_cls_hiddens = outs[1]  # (N, bert_embed_size)
        Y2_embeddings = self.linear.forward(Y1_cls_hiddens)  # (N, idiom2vec_embed_size)
        return Y2_embeddings

    # this is for inference.
    def idiomify(self, phrase: str, bert_tokenizer: BertTokenizer, idiom2vec: Word2Vec) -> List[Tuple[str, float]]:
        """
        given a query, this returns a
        :param phrase:
        :param bert_tokenizer:
        :param idiom2vec:
        :return:
        """
        # we don't need padding, because it is just only one phrase.
        batch_encoding = bert_tokenizer(phrase, return_tensors='pt')
        # build a 3-dimensional tensor. (1, 3, length)
        X = torch.Tensor([
            [batch_encoding['input_ids'],
             batch_encoding['token_type_ids'],
             batch_encoding['attention_mask']]
        ])
        phrase_vector = self.forward(X)[0]  # get the first one.
        # phrase similar by vector.
        sim_idioms = [
            (word, score)
            for word, score in idiom2vec.wv.similar_by_vector(vector=phrase_vector.numpy(), topn=None)
            if word in self.idioms  # only get those that are idioms.
        ]
        return sim_idioms


