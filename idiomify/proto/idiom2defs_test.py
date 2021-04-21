from idiomify.loaders import load_idiom2defs


def main():
    for idiom, def1, def2 in load_idiom2defs():
        print(idiom)
        print(def1, def2)


if __name__ == '__main__':
    main()
