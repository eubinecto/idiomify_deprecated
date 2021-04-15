import json
from typing import List
from idiomify.loaders import TsvTuplesLoader
from idiomify.paths import LINGUA_DEFS_TSV, LINGUA_RAWS_TSV
import re
import csv


def get_raw_defs(raw: dict) -> List[str]:
    # get the lexemes
    lexemes = [
        entry['lexemes']
        for entry in raw['entries']
    ]
    # get the senses
    senses = [
        lexeme_entry['senses']
        for lexeme in lexemes
        for lexeme_entry in lexeme
    ]
    # return the raw defs
    return [
        sense_entry['definition']
        for sense in senses
        for sense_entry in sense
    ]


def cleanse(raw_def: str) -> str:
    """
    e.g.
    '(by extension) the British government']
    [  '(Classical mythology) Elysium; home of the blessed, after death.',
    :param raw_def:
    :return:
    """
    return re.sub(r'\(.+?\)', "", raw_def).strip()


def split(raw_def: str) -> List[str]:
    """
    e.g.
    ['A large amount; a lot.', 'Very much; to a great extent; a lot; lots.']
    :param raw_def:
    :return:
    """
    return [
        entry.strip()
        for entry in raw_def.split(";")
    ]


def main():
    lingua_raws = TsvTuplesLoader().load(LINGUA_RAWS_TSV)
    with open(LINGUA_DEFS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, raw in lingua_raws:
            raw_defs = get_raw_defs(raw)
            cleansed = [
                cleanse(raw_def)
                for raw_def in raw_defs
            ]
            defs = [
                entry
                for raw_def in cleansed
                for entry in split(raw_def)
            ]
            to_write = [idiom, json.dumps(defs)]
            tsv_writer.writerow(to_write)


if __name__ == '__main__':
    main()
