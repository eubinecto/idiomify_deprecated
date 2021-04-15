"""
Will experiment with different models.
Starting Lstm as the baseline. - this is mainly for learning experience.
Compare that with Bert. - should be better than lstm.
Compare that with SBert. - should be better than Bert.
Compare that with SBertEnhanced. (extracting pos representations). - should be better than SBert alone.
"""
from typing import List, Tuple, Optional, Dict

import numpy as np
import torch
from gensim.models import KeyedVectors
from transformers import BertModel, BertTokenizer
from idiomify.datasets import encode_phrase


class BertIdiomifier(torch.nn.Module):
    """
    try this with Sentence BERT for encoding a sentence.
    https://arxiv.org/abs/1908.10084
    """
    def __init__(self, bert_embed_size: int, idiom2vec_embed_size: int,
                 bert_model: Optional[BertModel] = None):
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
        :param X_batch: (N, 3, M). 3 dimensional tensor. column 0: token ids, column 1: token type,
         column 3: pos encoding.
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
                 bert_tokenizer: BertTokenizer,
                 idionly2vec: KeyedVectors) -> List[Tuple[str, float]]:
        """
        given a query, this returns idioms that best match the phrase.
        :param phrase:
        :param bert_tokenizer:
        :param idionly2vec:
        :return:
        """
        X = encode_phrase(phrase, bert_tokenizer)
        phrase_vector = torch.squeeze(self.forward(X)).detach().numpy()
        idiom2sim = idionly2vec.similar_by_vector(phrase_vector)
        return idiom2sim
