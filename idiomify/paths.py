from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
ROOT_DIR = LIB_DIR.parent
DATA_DIR = ROOT_DIR.joinpath("data")
DEFS_DIR = DATA_DIR.joinpath("defs")
KEYS_DIR = DATA_DIR.joinpath("keys")
SLIDE_DIR = DATA_DIR.joinpath("slide")
IDIOM2VEC_DIR = DATA_DIR.joinpath("idiom2vec")
DEF2EMBED_DIR = DATA_DIR.joinpath('def2embed')
IDIOMIFIER_DIR = DATA_DIR.joinpath('idiomifier')


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
TARGET_IDIOMS_TXT = SLIDE_DIR.joinpath("target_idioms.txt")  # just a list of target idioms


# files - idiom2vec
IDIOM2VEC_MODEL = IDIOM2VEC_DIR.joinpath("idiom2vec_001.model")
IDIONLY2VEC_KV = IDIOM2VEC_DIR.joinpath("idionly2vec_001.kv")
TARGET_EMBEDDINGS_TSV = IDIOM2VEC_DIR.joinpath("target_embeddings.tsv")  # (idiom, embeddings)

# files - def2embed
DEF2EMBED_ALL_TSV = DEF2EMBED_DIR.joinpath("def2embed_all.tsv")  # (def, embed)
DEF2EMBED_TRAIN_TSV = DEF2EMBED_DIR.joinpath("def2embed_train.tsv")
DEF2EMBED_TEST_TSV = DEF2EMBED_DIR.joinpath("def2embed_test.tsv")


# files - idiomifier
S_BERT_IDIOMIFIER_001 = IDIOMIFIER_DIR.joinpath('s_bert_idiomifier_001.model')  # 001, first iteration.
