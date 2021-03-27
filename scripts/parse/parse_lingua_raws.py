from idiomify.loaders import load_raws
import pprint


def main():
    pp = pprint.PrettyPrinter(indent=3)
    lingua_raws = load_raws(name='lingua')
    for idiom, raws in lingua_raws[:100]:
        print("###" + idiom)
        pp.pprint(raws)


if __name__ == '__main__':
    main()
