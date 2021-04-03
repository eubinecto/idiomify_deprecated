"""
Will experiment with different models.
Starting Lstm as the baseline. - this is mainly for learning experience.
Compare that with Bert. - should be better than lstm.
Compare that with SBert. - should be better than Bert.
Compare that with SBertEnhanced. (extracting pos representations). - should be better than SBert alone.
"""

import torch


class Idiomifier(torch.nn.Module):

    def idiomify(self, query: str):
        """
        This is the target function to implement, basically.
        :param query:
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

    def idiomify(self, query: str):
        pass


class BertIdiomifier(Idiomifier):
    """
    uses vanilla BERT_NAME for encoding a sentence.
    https://arxiv.org/abs/1810.04805
    """

    def idiomify(self, query: str):
        pass


class SBertIdiomifier(Idiomifier):
    """
    uses Sentence BERT_NAME for encoding a sentence.
    https://arxiv.org/abs/1908.10084
    """

    def idiomify(self, query: str):
        pass

