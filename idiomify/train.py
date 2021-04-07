"""
the python script for training an idiomifier.

"""

from transformers import BertModel, BertTokenizer
from idiomify.idiomifiers import BertIdiomifier
from idiomify.loaders import load_target_idioms, load_def2embed
from idiomify.datasets import Def2EmbedDataset
from idiomify.paths import S_BERT_IDIOMIFIER_001
from torch.utils.data import DataLoader
import torch
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bert_model_name',
                        type=str,
                        default="deepset/sentence_bert")
    parser.add_argument('--bert_embed_size',
                        type=int,
                        default=768)
    parser.add_argument('--idiom2vec_embed_size',
                        type=int,
                        default=100)
    parser.add_argument('--batch_size',
                        type=int,
                        default=20)
    parser.add_argument('--epochs',
                        type=int,
                        default=10)
    parser.add_argument('--learning_rate',
                        type=float,
                        default=1e-5)
    parser.add_argument('--save_path',
                        type=str,
                        default=S_BERT_IDIOMIFIER_001)
    args = parser.parse_args()
    # TODO: use tensorboard to visualise the training progress.

    # --- gpu setup --- #
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # --- prepare the dataset --- #
    sent_bert_tokenizer = BertTokenizer.from_pretrained(args.bert_model_name)
    def2embed_train = load_def2embed('train')
    defs_train = [def_ for def_, _ in def2embed_train]
    embeds_train = [embed for _, embed in def2embed_train]
    # torch TensorDataset
    def2embed_dataset = Def2EmbedDataset(defs_train, embeds_train, sent_bert_tokenizer)
    # torch DataLoader. Has got some nice utilities.
    def2embed_dataloader = DataLoader(def2embed_dataset,
                                      batch_size=args.batch_size,
                                      shuffle=True)

    # --- prepare the model --- #
    sent_bert = BertModel.from_pretrained(args.bert_model_name)  # load a pretrained model
    target_idioms = load_target_idioms(norm=True)  # just to implement idiomify.
    idiomifier = BertIdiomifier(bert_model=sent_bert,
                                bert_embed_size=args.bert_embed_size,
                                idiom2vec_embed_size=args.idiom2vec_embed_size,
                                # need this for idiomify method.
                                # maybe..include this within idiom2vec?
                                # you could subclass Word2Vec.
                                idioms=target_idioms)
    idiomifier = idiomifier.to(device)  # transfer the net to cuda/cpu.

    # --- prepare the optimizer & loss --- #
    adam_optim = torch.optim.Adam(idiomifier.parameters(),
                                  lr=args.learning_rate)  # we use adam optimizer
    cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)  # for now, use simple cosine sim.

    # --- train the model --- #
    idiomifier.train()  # put the model in a training mode
    for epoch in range(args.epochs):
        for batch_idx, batch in enumerate(def2embed_dataloader):
            X_batch = batch[0]  # the batch to compute the loss for
            Y = batch[1]  # the labels for the batch
            # remember to send the inputs and targets to the device as well
            X_batch = X_batch.to(device)
            Y = Y.to(device)
            # forward pass
            Y_hat = idiomifier.forward(X_batch)  # predicted value
            loss = torch.sum(1 - cos(Y, Y_hat))  # sum up all the loss for this batch
            print("epoch: {}, batch: {}, loss: {}".format(epoch, batch_idx, loss.item()))
            # reset the gradients
            # this is to clear the buffer
            adam_optim.zero_grad()
            # backward propagation; backward gradients are computed
            loss.backward()
            # update the weights with gradient descent
            adam_optim.step()

    # then save the model
    torch.save(idiomifier.state_dict(), args.save_path)


if __name__ == '__main__':
    main()
