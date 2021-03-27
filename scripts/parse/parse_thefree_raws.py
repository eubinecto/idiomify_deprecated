"""
somethings to do.
## as for cleansing
1. get rid of anything that's inside []
e.g.  [Colloquial; mid-1900s]
e.g. [Early 1900s]
e.g. [c. 1940]

2. remove "Also,", does not add much to the definition.  remove "Also see", and "See also" as well. remove "See" (it is sometimes used alone).
e.g. Also, in the slightest.
e.g. See for the devil of it (See being used alone)


3. get rid of colon.
e.g.  At a low price:


2. remove [Colloquial; ...]. Timeliness does not add that much to the definition.
e.g.  [Colloquial; mid-1900s]
e.g.  [Colloquial; early 1900s]


2. the numbers. get rid of them (results from ds-lists)
e.g. 1. To aim..
e.g. 2. To get..

3. the quotation marks - replace that with an empty space. wait, I'm not sure what to do with this. Could do some research on this?
 but maybe later.
e.g. Typically used in the phrase "nothing to write home about,"

4. stripe "Fig." and "Lit.", "mod." out. remove "exclam."
e.g. Fig. very valuable.
e.g. 1. . Lit. to wiggle and squeeze out of something or some place.
e.g. mod. with no problem(s).
e.g.  mod. flamboyantly; boldly.
e.g.  exclam.
-> how could you characterize them...?



5. get rid of the collocations. These are characterized by the format: (*Typically: ...).
I don't need them, as I'll be extracting them by myself.
e.g. (*Typically: be ~ become ∼.)
e.g. (*Typically: do something ~ sit ~ walk ∼.)
e.g. (*Typically: go ∼.)

5. parenthesis - just remove them
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


3. remove "COMMON". case-sensitive.
e.g. 3. injured.
COMMON
e.g. COMMON If you have the worst of both worlds


"""


from idiomify.loaders import load_raws


def cleanse(raw: str) -> str:
    pass


def main():
    thefree_raws = load_raws("thefree")

    for idiom, raws in thefree_raws:
        print("###" + idiom)
        for raw in raws:
            print(raw)

if __name__ == '__main__':
    main()