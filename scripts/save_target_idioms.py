from idiomify.loaders import load_slide_idioms
from idiomify.paths import TARGET_IDIOMS_TXT

TARGET_IDIOM_MIN_LENGTH = 14
TARGET_IDIOM_MIN_WORD_COUNT = 3

IGNORED_CASES = (
    "Number Ten",  # duplicate ->  Number 10 exists.
    "if needs be",  # duplicate ->  "if need be" is enough. pattern matching with lemmas will cover this case.
    "ride the ... train",  # doesn't have a dedicated wiktionary entry.
    "above and beyond the call of duty",  # the page has been deleted.
    "be absorbed by",  # this one is also deleted
)

MORE_CASES = {
    "have blood on one's hands",
    "come down to earth"
}


def is_target(idiom: str) -> bool:
    global TARGET_IDIOM_MIN_LENGTH, TARGET_IDIOM_MIN_LENGTH, IGNORED_CASES

    def above_min_word_count(idiom_: str) -> bool:
        return len(idiom_.split(" ")) >= TARGET_IDIOM_MIN_WORD_COUNT

    def above_min_length(idiom_: str) -> bool:
        return len(idiom_) >= TARGET_IDIOM_MIN_LENGTH

    def is_hyphenated(idiom_: str) -> bool:
        return "-" in idiom_

    return (idiom not in IGNORED_CASES) \
           and (above_min_word_count(idiom) or
                above_min_length(idiom) or
                is_hyphenated(idiom))


def main():
    global MORE_CASES

    target_idioms = [
        idiom
        for idiom in load_slide_idioms()
        if is_target(idiom)
    ]
    target_idioms += MORE_CASES

    with open(TARGET_IDIOMS_TXT, 'w') as fh:
        for target in target_idioms:
            fh.write(target + "\n")


if __name__ == '__main__':
    main()
