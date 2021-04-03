
from idiomify.loaders import load_defs
import pprint


def main():
    merged_defs = load_defs('merged')
    pp = pprint.PrettyPrinter(indent=3)
    for idiom, defs in merged_defs:
        print("###" + idiom)
        for entry in defs:
            print(entry)


if __name__ == '__main__':
    main()
