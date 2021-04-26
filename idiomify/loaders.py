import json
from functional import seq
from functional.pipeline import Sequence
from idiomify.paths import IDIOM2SYNS_CSV


def load_idiom2syns() -> Sequence:
    return seq.csv(IDIOM2SYNS_CSV, delimiter=",") \
              .map(lambda row: (row[0].strip().replace("\ufeff", ""),
                                row[3]))
