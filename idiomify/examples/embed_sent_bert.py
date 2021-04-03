"""
encoding a sentence into a vector with BERT_NAME.
How do I do this..?
Somebody asked this here:
https://stackoverflow.com/questions/63461262/bert-sentence-embeddings-from-transformers
where does 6 come from?
-> "The original Transformer contains a stack of N=6 layers.".  That is the number of layers
 in BERT_NAME.
"""
from typing import Tuple

from transformers import BatchEncoding
from transformers.models.bert import BertModel,\
                                     BertTokenizer


# Vanilla Bert
# 12-layer, 768-hidden, 12-heads, 110M parameters.
# Trained on lower-cased English text.
BERT_NAME = "bert-base-uncased"
# Sentence Bert
# optimized for encoding a single sentence.
S_BERT_NAME = "deepset/sentence_bert"  # Sentence - Bert.
# example text
TEXT = "to avoid being straightforward"


def load_tok_and_bert(name: str) -> Tuple[BertTokenizer, BertModel]:
    tokenizer = BertTokenizer.from_pretrained(name)
    model = BertModel.from_pretrained(name)
    return tokenizer, model


def encode_text(tokenizer: BertTokenizer, text: str) -> BatchEncoding:
    encoded = tokenizer(text, return_tensors='pt')  # return as a pytorch tensor
    print("-------encode_text")
    print("input_ids: " + str(encoded.data['input_ids']))  # str -> int encoded values
    print("token_type_ids: " + str(encoded.data['token_type_ids']))  # which sentence does it belong to?
    print("attention_mask: " + str(encoded.data['attention_mask']))  # which token should it attend to?
    input_ids = encoded.data['input_ids'][0]  # squeeze the dimension
    print("decoded: " + tokenizer.decode(token_ids=input_ids))  # [CLS], [SEP] tokens will be added.
    return encoded


def main():
    global BERT_NAME, S_BERT_NAME, TEXT
    # should use the tokenizer that was used to train the pre-trained model.
    bert_tokenizer, bert = load_tok_and_bert(BERT_NAME)
    s_bert_tokenizer, s_bert = load_tok_and_bert(S_BERT_NAME)
    # encode the inputs.
    encoded_for_bert = encode_text(bert_tokenizer, TEXT)
    encoded_for_s_bert = encode_text(s_bert_tokenizer, TEXT)
    # forward pass.
    embedded_with_bert = bert(**encoded_for_bert)
    embedded_with_s_bert = s_bert(**encoded_for_s_bert)
    print("--------embedded with bert")
    print(embedded_with_bert[0].shape)  # tokens_hidden - hidden representations for each token (e.g. [1, 6, 768])
    print(embedded_with_s_bert[1].shape)  # cls_hidden - hidden representation for the [CLS] token (e.g. [1, 768])

    print("--------embedded with s bert")
    print(embedded_with_bert[0].shape)  # tokens_hidden - hidden representations for each token (e.g. [1, 6, 768])
    print(embedded_with_s_bert[1].shape)  # cls_hidden - hidden representation for the [CLS] token (e.g. [1, 768])


if __name__ == '__main__':
    main()
