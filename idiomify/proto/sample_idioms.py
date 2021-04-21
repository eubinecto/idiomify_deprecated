
from identify_idioms.service import load_idioms
import random

SIZE = 100
SEED = 318
random.seed(SEED)


def main():
    idioms = [idiom.replace(" " , "_") for idiom in load_idioms()]
    sampled = random.sample(idioms, SIZE)
    for sample in sampled:
        print(sample)


if __name__ == '__main__':
    main()
