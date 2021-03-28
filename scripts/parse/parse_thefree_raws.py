"""
somethings to do.
## as for cleansing
1. get rid of anything that's inside []
e.g.  [Colloquial; mid-1900s]
e.g. [Early 1900s]
e.g. [c. 1940]

1. includes... remove [Colloquial; ...]. Timeliness does not add that much to the definition.
e.g.  [Colloquial; mid-1900s]
e.g.  [Colloquial; early 1900s]


2. remove "Also,", does not add much to the definition.  remove "Also see", and "See also" as well. remove "See" (it is sometimes used alone).
e.g. Also, in the slightest.
e.g. See for the devil of it (See being used alone)


3. get rid of colon.
e.g.  At a low price:

4. remove "COMMON". case-sensitive.
e.g. 3. injured.
COMMON
e.g. COMMON If you have the worst of both worlds


5. the numbers for listing. get rid of them (results from ds-lists)
e.g. 1. To aim..
e.g. 2. To get..



6. stripe "Fig." and "Lit.", "mod." out. remove "exclam."
e.g. Fig. very valuable.
e.g. 1. . Lit. to wiggle and squeeze out of something or some place.
e.g. mod. with no problem(s).
e.g.  mod. flamboyantly; boldly.
e.g.  exclam.
-> how could you characterize them...?



7. get rid of the collocations. These are characterized by the format: (*Typically: ...).
I don't need them, as I'll be extracting them by myself.
e.g. (*Typically: be ~ become ∼.)
e.g. (*Typically: do something ~ sit ~ walk ∼.)
e.g. (*Typically: go ∼.)

8. parenthesis - just remove them
e.g. problem(s)
e.g. Erasmus in the sixteenth century (in Latin).
e.g. Don't expect something to happen. (The idea being that one couldn't hold one's breath long enough for the unlikely thing to happen.)

## as for parsing the definitions

1. treat every single sentence, delimited by ".", as the definition. This even includes "For example, ~" ..
2. semicolon is also a strong delimiter for definitions
e.g.
Every year; year after year.
year after year; for years.
these are four definitions, in two sentences.


## things I'm not sure about.
The quotation marks - replace that with an empty space. wait, I'm not sure what to do with this. Not sure about this hough
 but maybe later.
e.g. Typically used in the phrase "nothing to write home about,"

"""
import json
from typing import List
from idiomify.paths import THEFREE_DEFS_TSV
from idiomify.loaders import load_raws
import re
import csv


def remove_brackets(raw: str) -> str:
    """
    remove anything inside brackets.
    :param raw:
    :return:
    """
    return re.sub(r'\[.+?\]', "", raw).strip()


def remove_typically(raw: str) -> str:
    """
     (*Typically be ~; have ~.)
    :param raw:
    :return:
    """
    return re.sub(r'\(\*Typically.*\)', "", raw).strip()


def remove_parenthesis(raw: str) -> str:
    raw = raw.replace("(", "")
    raw = raw.replace(")", "")
    return raw.strip()


def remove_also(raw: str) -> str:
    """
    # make sure they are case sensitive.
    "Also,"
    "Also see"
    "See also"
    "See"
    """
    return re.sub(r'Also,|Also|Also see|See also|See|Note', "", raw).strip()


def remove_colon(raw: str) -> str:
    return raw.replace(":", "").strip()


def remove_common(raw: str) -> str:
    return raw.replace("COMMON", "").strip()


def remove_numbering(raw: str) -> str:
    return re.sub(r'[1-9]\. ', "", raw).strip()


def remove_dangling_dots(raw: str) -> str:
    return re.sub(r' \. |^\. ', "", raw).strip()


def remove_quotation_marks(raw: str) -> str:
    return raw.replace("\"", "").strip()


def remove_extras(raw: str) -> str:
    return re.sub(r'^[a-zA-Z]+\. ', "", raw).strip()


def exceptions(raw: str) -> str:
    return raw.replace("] Colloquial; 1960s]", "").strip()


def cleanse(raw: str) -> str:
    """
    preprocess the texts.
    :param raw:
    :return:
    """
    raw = remove_brackets(raw)
    raw = remove_typically(raw)
    raw = remove_parenthesis(raw)  # should do this after removing (*Typically)
    raw = remove_also(raw)
    raw = remove_colon(raw)
    raw = remove_common(raw)
    raw = remove_numbering(raw)
    raw = remove_dangling_dots(raw)
    raw = remove_extras(raw)
    raw = remove_quotation_marks(raw)
    raw = exceptions(raw)  # anything that need to be replaced
    return raw


def parse(raw: str) -> List[str]:
    """
    parse the raw to get a list of definitions.
    :param raw:
    :return:
    """
    # delimit the raw with either a dot, or a semicolon.
    return [
        definition.strip()
        for definition in re.split(r'[.;]', raw)
        if definition and len(definition) > 3
    ]


def main():
    thefree_raws = load_raws("thefree")
    # cleanse them.
    thefree_cleansed = [
        (idiom, [cleanse(raw) for raw in raws if cleanse(raw)])
        for idiom, raws in thefree_raws
    ]
    thefree_defs = [
        (idiom, [definition for raw in raws for definition in parse(raw)])
        for idiom, raws in thefree_cleansed
    ]

    with open(THEFREE_DEFS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        for idiom, defs in thefree_defs:
            tsv_writer.writerow([idiom, json.dumps(defs)])


if __name__ == '__main__':
    main()
