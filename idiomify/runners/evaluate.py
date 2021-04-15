from typing import List, Tuple
import numpy as np
from gensim.models import KeyedVectors
from tqdm import tqdm
from transformers import BertTokenizer, BertModel
from idiomify.idiomifiers import BertIdiomifier
from idiomify.loaders import TsvTuplesLoader
import torch
import argparse


def evaluate_idiomifier(idiomifier: BertIdiomifier,
                        idionly2vec: KeyedVectors,
                        bert_tokenizer: BertTokenizer,
                        def2embed_to_test: List[Tuple[str, List[float]]]) -> float:
    total = len(def2embed_to_test)
    correct = 0
    for phrase, embed in tqdm(def2embed_to_test):
        embed_vec = np.array(embed)
        idiom_hat = idiomifier.idiomify(phrase, bert_tokenizer, idionly2vec)[0][0]  # the predicted one
        idiom = idionly2vec.similar_by_vector(embed_vec, topn=1)[0][0]  # the correct one
        # we only consider the top one.
        if idiom_hat == idiom:  # are they equal?
            correct += 1
    # return the accuracy
    return correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bert_model_name',
                        type=str,
                        default="deepset/sentence_bert")
    parser.add_argument('--idiomifier_model_path',
                        type=str,
                        default="../../data/idiomifier/s_bert_idiomifier_001.model")
    parser.add_argument('--idionly2vec_kv_path',
                        type=str,
                        default="../../data/idiom2vec/idionly2vec_001.kv")
    parser.add_argument('--def2embed_train_tsv_path',
                        type=str)
    parser.add_argument('--def2embed_test_tsv_path',
                        type=str,
                        default="../../data/def2embed/def2embed_test.tsv")
    args = parser.parse_args()

    # --- cuda setup --- #
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # --- load the models --- #
    bert_tokenizer = BertTokenizer.from_pretrained(args.bert_model_name)
    s_bert_model = BertModel.from_pretrained(args.bert_model_name)  # still need to load the entire thing?
    idiomifier = BertIdiomifier(768, 100, s_bert_model)
    idiomifier.load_state_dict(torch.load(args.idiomifier_model_path, map_location=device))
    idionly2vec = KeyedVectors.load_word2vec_format(args.idionly2vec_kv_path, binary=False)

    # --- load the test set --- #
    def2embed_test = TsvTuplesLoader().load(args.def2embed_test_tsv_path)
    test_acc = evaluate_idiomifier(idiomifier, idionly2vec, bert_tokenizer, def2embed_test)
    print(test_acc)


if __name__ == '__main__':
    main()
