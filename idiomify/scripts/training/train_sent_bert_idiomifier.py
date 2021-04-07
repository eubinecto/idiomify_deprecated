from dataclasses import dataclass
from transformers import BertModel, BertTokenizer
from idiomify.idiomifiers import BertIdiomifier
from idiomify.loaders import load_target_idioms, load_def2embed
from torch.utils.data import TensorDataset


@dataclass
class Metadata:
    bert_model_name: str
    bert_embed_size: int
    idiom2vec_embed_size: int
    idiom2vec_ver: str
    batch_size: int
    epochs: int
    learning_rate: float


# metadata
METADATA = Metadata(bert_model_name="deepset/sentence_bert",
                    bert_embed_size=768,
                    idiom2vec_embed_size=100,
                    idiom2vec_ver='0.0.1',
                    batch_size=10,
                    epochs=10,
                    learning_rate=1e-5)


def main():
    global METADATA

    # --- prepare model ---- #
    sent_bert = BertModel.from_pretrained(METADATA.bert_model_name)
    sent_bert_tok = BertTokenizer.from_pretrained(METADATA.bert_model_name)
    target_idioms = load_target_idioms(norm=True)
    # put the bert in train mode.
    sent_bert.train()
    sent_bert_idiomifier = BertIdiomifier(sent_bert, sent_bert_tok,
                                          METADATA.bert_embed_size,
                                          METADATA.idiom2vec_embed_size,
                                          target_idioms)

    # --- prepare dataset --- #
    def2embed_train = load_def2embed('train')
    def2embed_train_dataset = TensorDataset()

    for epoch in range(METADATA.epochs):
        # train.. for each epoch.
        # report the progress somewhere...?
        pass


if __name__ == '__main__':
    main()
