from functional import seq
from functional.pipeline import Sequence
from idiomify.paths import IDIOM2DEF_TSV, IDIOM2SYNS_TSV


def load_idiom2def() -> Sequence:
    return seq.csv(IDIOM2DEF_TSV, delimiter="\t") \
              .map(lambda row: (row[0],
                                # the second column in freq.
                                row[2]))


def load_idiom2syns() -> Sequence:
    return seq.csv(IDIOM2SYNS_TSV, delimiter="\t") \
              .map(lambda row: (row[0],
                                # the second column in freq.
                                row[2]))
