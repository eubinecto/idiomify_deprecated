"""
just to have a look at the final dataset.
"""

from idiomify.loaders import TsvTuplesLoader
from idiomify.paths import MERGED_DEFS_TSV


def main():
    merged_defs = TsvTuplesLoader().load(MERGED_DEFS_TSV)
    for idiom, defs in merged_defs:
        print("###" + idiom)
        for entry in defs:
            print(entry)
    print(len(merged_defs))


if __name__ == '__main__':
    main()
