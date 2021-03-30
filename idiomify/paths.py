from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
ROOT_DIR = LIB_DIR.parent
DATA_DIR = ROOT_DIR.joinpath("data")
DEFS_DIR = DATA_DIR.joinpath("defs")
KEYS_DIR = DATA_DIR.joinpath("keys")
SLIDE_DIR = DATA_DIR.joinpath("slide")
IDIOM2VEC_DIR = DATA_DIR.joinpath("idiom2vec")


# files - data
TARGET_IDIOMS_TXT = DATA_DIR.joinpath("target_idioms.txt")  # just a list of target idioms
TARGET_EMBEDDINGS_TSV = DATA_DIR.joinpath("target_embeddings.tsv")  # (idiom, embeddings)
DEF2EMBED_TSV = DATA_DIR.joinpath("def2embed.tsv")  # (def, embed)

# files - defs
URBAN_RAWS_TSV = DEFS_DIR.joinpath("urban_raws.tsv")  # collection of raw data (idiom, resp)
URBAN_DEFS_TSV = DEFS_DIR.joinpath("urban_defs.tsv")  # the raw definitions parsed to (idiom, defs)
LINGUA_RAWS_TSV = DEFS_DIR.joinpath("lingua_raws.tsv")  # from lingua api, raw responses
LINGUA_DEFS_TSV = DEFS_DIR.joinpath("lingua_defs.tsv")  # from lingua api, cleansed and parsed.
WORDNIK_RAWS_TSV = DEFS_DIR.joinpath("wordnik_raws.tsv")
THEFREE_RAWS_TSV = DEFS_DIR.joinpath("thefree_raws.tsv")
THEFREE_DEFS_TSV = DEFS_DIR.joinpath("thefree_defs.tsv")
MERGED_DEFS_TSV = DEFS_DIR.joinpath("merged_defs.tsv")


# files - keys
RAPID_KEY_TXT = KEYS_DIR.joinpath("rapid_key.txt")
WORDNIK_KEY_TXT = KEYS_DIR.joinpath("wordnik_key.txt")


# files - slide
SLIDE_TSV = SLIDE_DIR.joinpath("slide.tsv")


# files - idiom2vec
IDIOM2VEC_MODEL = IDIOM2VEC_DIR.joinpath("idiom2vec_001.model")
