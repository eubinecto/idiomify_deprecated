from typing import Tuple, List
from torch.utils.data import Dataset
from transformers import BertTokenizer
import torch


# --- utils --- #
def encode_phrase(phrase: str, bert_tokenizer: BertTokenizer) -> torch.Tensor:
    # we don't need padding, because it is just only one phrase.
    batch_encoding = bert_tokenizer(phrase, return_tensors='pt')
    # build a 3-dimensional tensor. (1, 3, length)
    X = torch.stack((batch_encoding['input_ids'],
                     batch_encoding['token_type_ids'],
                     batch_encoding['attention_mask']), 1) \
        .type(torch.IntTensor)
    return X


def encode_phrases(phrases: List[str], bert_tokenizer: BertTokenizer) -> torch.IntTensor:
    encodings = bert_tokenizer(phrases,
                               # return as pytorch tensors
                               return_tensors='pt',
                               # apply padding
                               padding=True)
    # access the encodings.
    input_ids = encodings['input_ids']  # (N, M)
    token_type_ids = encodings['token_type_ids']  # (N, M)
    attention_masks = encodings['attention_mask']  # (N, M)
    # combine them into a pytorch tensor
    X: torch.IntTensor = torch.stack((input_ids,
                                      token_type_ids,
                                      attention_masks), 0) \
                              .type(torch.IntTensor)  # 3D int tensor. (3, N, M)
    return X


# --- the dataset --- #
class Def2EmbedDataset(Dataset):
    def __init__(self,
                 defs: List[str],
                 embeds: List[List[float]],
                 bert_tokenizer: BertTokenizer):
        """
        For preprocessing
        :param defs:
        :param embeds:
        :param bert_tokenizer:
        """
        # just make sure they are of the same size.
        assert len(defs) == len(embeds)
        self.X: torch.IntTensor = encode_phrases(defs, bert_tokenizer)
        self.Y: torch.FloatTensor = torch.FloatTensor(embeds)  # 2D float tensor. (N, idiom2vec_embed_size)

    def __len__(self) -> int:
        """
        Returning the size of the dataset
        :return:
        """
        return self.Y.shape[0]

    def __getitem__(self, idx: int) -> Tuple[torch.IntTensor, torch.FloatTensor]:
        """
        Returns features & the label

        :param idx:
        :return:
        """
        X_encodings = self.X[:, idx]  # (3, M)
        y = self.Y[idx]  # (1, idiom2vec_embed_size)
        return X_encodings, y
