"""
just to have a look at the final dataset.
"""

from idiomify.loaders import load_defs


def main():
    merged_defs = load_defs('merged')
    for idiom, defs in merged_defs:
        print("###" + idiom)
        for entry in defs:
            print(entry)
    print(len(merged_defs))


if __name__ == '__main__':
    main()
