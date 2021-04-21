import json
from functional import seq
from functional.pipeline import Sequence
from idiomify.paths import IDIOM2DEFS_CSV


def load_idiom2defs() -> Sequence:
    return seq.csv(IDIOM2DEFS_CSV, delimiter=",") \
              .map(lambda row: (row[0],
                                row[1],
                                row[2]))
