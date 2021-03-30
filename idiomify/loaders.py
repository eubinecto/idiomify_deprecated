from typing import List, Tuple, Union
from idiomify.paths import (
    SLIDE_TSV,
    TARGET_IDIOMS_TXT,
    RAPID_KEY_TXT,
    WORDNIK_KEY_TXT,
    URBAN_RAWS_TSV,
    LINGUA_RAWS_TSV,
    THEFREE_RAWS_TSV, LINGUA_DEFS_TSV, THEFREE_DEFS_TSV, MERGED_DEFS_TSV
)
import csv
import json


def load_slide_idioms() -> List[str]:
    idioms = list()
    with open(SLIDE_TSV, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        # skip the header
        next(tsv_reader)  # skip the header
        for row in tsv_reader:
            idiom = row[0]
            idioms.append(idiom)
    return idioms


def load_target_idioms() -> List[str]:
    idioms = list()
    with open(TARGET_IDIOMS_TXT, 'r') as fh:
        for line in fh:
            idioms.append(line.strip())
    return idioms


# loading the raw responses, to be used for parsing.
def load_raws(name: str) -> List[Tuple[str, Union[list, dict]]]:
    if name == "urban":
        tsv_path = URBAN_RAWS_TSV
    elif name == "lingua":
        tsv_path = LINGUA_RAWS_TSV
    elif name == "thefree":
        tsv_path = THEFREE_RAWS_TSV
    else:
        raise ValueError("Invalid name:" + name)
    # collect the raw files and return
    rows = list()
    with open(tsv_path, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        # no header, just start reading
        for row in tsv_reader:
            idiom = row[0]
            raws = json.loads(row[1])
            rows.append((idiom, raws))
    return rows


def load_defs(name: str) -> List[Tuple[str, List[str]]]:
    if name == "lingua":
        tsv_path = LINGUA_DEFS_TSV
    elif name == "thefree":
        tsv_path = THEFREE_DEFS_TSV
    elif name == "merged":
        tsv_path = MERGED_DEFS_TSV
    else:
        raise ValueError("Invalid name:" + name)
    # collect the raw files and return
    rows = list()
    with open(tsv_path, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        # no header, just start reading
        for row in tsv_reader:
            idiom = row[0]
            defs = json.loads(row[1])
            rows.append((idiom, defs))
    return rows


# for api keys
def load_key(name: str) -> str:
    if name == "rapid":
        key_path = RAPID_KEY_TXT
    elif name == "wordnik":
        key_path = WORDNIK_KEY_TXT
    else:
        raise ValueError("Invalid name:" + name)
    with open(key_path, 'r') as fh:
        return fh.read().strip()
