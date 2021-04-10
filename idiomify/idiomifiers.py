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

    # this is for inference.
    def idiomify(self, phrase: str,
                 idioms: List[str],
                 bert_tokenizer: BertTokenizer,
                 idiom2vec: Word2Vec) -> List[Tuple[str, float]]:
        """
        This is the target function to implement, basically.
        :return:
        """
        raise NotImplementedError


class BertIdiomifier(Idiomifier):
    """
    try this with Sentence BERT for encoding a sentence.
    https://arxiv.org/abs/1908.10084
    """
    def __init__(self, bert_model: BertModel,
                 bert_embed_size: int, idiom2vec_embed_size: int):
        """
        :param bert_model: (pretrained) bert model to be used for encoding a phrase (sentence)
        :param idiom2vec_embed_size: should be the same as the output of idiom2vec model.
        """
        super().__init__()
        self.bert_embed_size = bert_embed_size
        self.idiom2vec_embed_size = idiom2vec_embed_size
        self.bert_model = bert_model  # sentence encoder layer
        self.linear = torch.nn.Linear(bert_embed_size, idiom2vec_embed_size)  # projection layer

    def forward(self, X_batch: torch.Tensor) -> torch.Tensor:
        """
        :param X_batch: (N, 3, M). 3 dimensional tensor. column 0: token ids, column 1: token type, column 3: pos encoding.
        :return:
        """
        X_token_ids = X_batch[:, 0]
        X_token_type_ids = X_batch[:, 1]
        X_attention_mask = X_batch[:, 2]
        # forward pass to the bert module
        outs = self.bert_model(input_ids=X_token_ids,
                               attention_mask=X_attention_mask,
                               token_type_ids=X_token_type_ids)
        # idx = 0: token_hidden, 1: cls_hidden
        Y1_cls_hiddens = outs[1]  # (N, bert_embed_size)
        Y2_embeddings = self.linear.forward(Y1_cls_hiddens)  # (N, idiom2vec_embed_size)
        return Y2_embeddings

    # this is for inference.
    def idiomify(self, phrase: str,
                 idioms: List[str],
                 bert_tokenizer: BertTokenizer,
                 idiom2vec: Word2Vec) -> List[Tuple[str, float]]:
        """
        given a query, this returns a
        :param phrase:
        :param idioms:
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
        # only one vector will come out, so squeeze it out.
        phrase_vector = torch.squeeze(self.forward(X))
        # phrase similar by vector.
        # TODO: maybe put this logic within idiom2vec model.
        sim_idioms = [
            (word, score)
            for word, score in idiom2vec.wv.similar_by_vector(vector=phrase_vector.numpy(), topn=None)
            if word in idioms  # only get those that are idioms.
        ]
        return sim_idioms