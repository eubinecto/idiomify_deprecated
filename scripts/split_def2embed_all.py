"""
split def2embed.tsv
into def2embed_train.tsv & def2embed_test.tsv
"""
import json
from typing import List

from sklearn.model_selection import train_test_split
from idiomify.loaders import TsvTuplesLoader
from idiomify.paths import DEF2EMBED_ALL_TSV, DEF2EMBED_TRAIN_TSV, DEF2EMBED_TEST_TSV
import csv


RANDOM_STATE = 318

# TODO: Implement upsampling & data augmentation (just simple copy and paste could work) later.
# remember, machine learning is algorithm AND data.


def write_set(defs: List[str], embeds: List[List[float]], tsv_path: str):
    with open(tsv_path, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for def_, embed in zip(defs, embeds):
            to_write = [def_, json.dumps(embed)]
            tsv_writer.writerow(to_write)


def main():
    global RANDOM_STATE
    def2embed_all = TsvTuplesLoader().load(DEF2EMBED_ALL_TSV)
    x = [def_ for def_, _ in def2embed_all]  # only the definitions
    y = [embed for _, embed in def2embed_all]  # only the embeds (labels)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
                                                        random_state=RANDOM_STATE)

    # write the train set
    write_set(defs=x_train, embeds=y_train, tsv_path=DEF2EMBED_TRAIN_TSV)
    write_set(defs=x_test, embeds=y_test, tsv_path=DEF2EMBED_TEST_TSV)


if __name__ == '__main__':
    main()
