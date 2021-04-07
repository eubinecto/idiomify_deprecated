"""
encoding a sentence into a vector with BERT_NAME.
How do I do this..?
Somebody asked this here:
https://stackoverflow.com/questions/63461262/bert-sentence-embeddings-from-transformers
where does 6 come from?
-> "The original Transformer contains a stack of N=6 layers.".  That is the number of layers
 in BERT_NAME.
"""
from typing import Tuple, List

from transformers import BatchEncoding
from transformers.models.bert import BertModel,\
                                     BertTokenizer


S_BERT_NAME = "deepset/sentence_bert"  # Sentence - Bert.
# example text
TEXTS = [
    "to avoid being straightforward",
    "to beat around the bush"
]


def load_tok_and_bert(name: str) -> Tuple[BertTokenizer, BertModel]:
    tokenizer = BertTokenizer.from_pretrained(name)
    model = BertModel.from_pretrained(name)
    return tokenizer, model


def main():
    global S_BERT_NAME, TEXTS
    # should use the tokenizer that was used to train the pre-trained model.
    s_bert_tokenizer = BertTokenizer.from_pretrained(S_BERT_NAME)
    s_bert = BertModel.from_pretrained(S_BERT_NAME)

    # encode the inputs.
    encoded_for_s_bert = s_bert_tokenizer(
        TEXTS,
        # return as pytorch tensor
        return_tensors='pt',
        #  padding and/or truncation is needed to have batched tensors with the same length.
        padding=True
    )
    print("-------encode_text")
    print("input_ids: " + str(encoded_for_s_bert['input_ids']))  # str -> int encoded values
    print("token_type_ids: " + str(encoded_for_s_bert['token_type_ids']))  # which sentence does it belong to?
    print("attention_mask: " + str(encoded_for_s_bert['attention_mask']))  # which token should it attend to?
    input_ids = encoded_for_s_bert.data['input_ids'][0]  # squeeze the dimension
    print("decoded: " + s_bert_tokenizer.decode(token_ids=input_ids))  # [CLS], [SEP] tokens will be added.

    # forward pass.
    embedded_with_s_bert = s_bert(**encoded_for_s_bert)

    print("--------embedded with s bert")
    print(embedded_with_s_bert[0].shape)  # tokens_hidden - hidden representations for each token (e.g. [1, 6, 768])
    print(embedded_with_s_bert[1].shape)  # cls_hidden - hidden representation for the [CLS] token (e.g. [1, 768])


if __name__ == '__main__':
    main()
