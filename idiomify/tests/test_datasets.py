from typing import List
from unittest import TestCase
from transformers import BertTokenizer
from idiomify.datasets import Def2EmbedDataset
from idiomify.loaders import load_def2embed


class Def2EmbedDatasetTest(TestCase):

    defs: List[str]
    embeds: List[List[float]]
    bert_tokenizer: BertTokenizer
    def2embed_dataset: Def2EmbedDataset

    @classmethod
    def setUpClass(cls) -> None:
        def2embed_train = load_def2embed('train')
        cls.bert_tokenizer = BertTokenizer.from_pretrained("deepset/sentence_bert")
        cls.defs = [def_ for def_, _ in def2embed_train]
        cls.embeds = [embed for _, embed in def2embed_train]
        cls.def2embed_dataset = Def2EmbedDataset(cls.defs, cls.embeds, cls.bert_tokenizer)

    def test_len(self):
        self.assertEqual(len(self.defs), len(self.def2embed_dataset))

    def test_X_dim(self):
        # the first dimension: input_ids, token_type_ids, attention masks
        self.assertEqual(3, self.def2embed_dataset.X.shape[0])
        # the second dimension: number of samples
        self.assertEqual(len(self.defs), self.def2embed_dataset.X.shape[1])
        # to test the last dimension, get the maximum length.
        max_def = max(self.defs, key=lambda x: len(x))
        max_encodings = self.bert_tokenizer(max_def, return_tensors='pt')
        max_length = max_encodings['input_ids'].shape[1]
        self.assertEqual(max_length, self.def2embed_dataset.X.shape[2])

    def test_Y_dim(self):
        # the first dimension: number of examples
        self.assertEqual(len(self.defs), self.def2embed_dataset.Y.shape[0])
        # the second dimension: the embedding size of idiom2vec
        self.assertEqual(100, self.def2embed_dataset.Y.shape[1])
