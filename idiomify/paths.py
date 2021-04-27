from os import path

# directories
HOME_DIR = path.expanduser("~")
DATA_DIR = path.join(HOME_DIR, 'data')
CORPORA_DIR = path.join(HOME_DIR, "corpora")  # this is always at home.
IDIOMS_DIR = path.join(CORPORA_DIR, "idioms")
DATA_IDIOM2VEC_DIR = path.join(DATA_DIR, "data_idiom2vec")
IDIOM2VEC_DIR = path.join(DATA_IDIOM2VEC_DIR, "idiom2vec")

# idiom2vec
IDIOM2VEC_WV_001_BIN = path.join(IDIOM2VEC_DIR, "idiom2vec_wv_001.bin")
IDIOM2VEC_WV_002_BIN = path.join(IDIOM2VEC_DIR, "idiom2vec_wv_002.bin")
IDIOM2VEC_WV_003_BIN = path.join(IDIOM2VEC_DIR, "idiom2vec_wv_003.bin")
IDIOM2VEC_WV_004_BIN = path.join(IDIOM2VEC_DIR, "idiom2vec_wv_004.bin")

# idioms
IDIOM2DEF_TSV = path.join(IDIOMS_DIR, 'idiom2def.tsv')
IDIOM2SYNS_TSV = path.join(IDIOMS_DIR, 'idiom2syns.tsv')

# spacy
NLP_MODEL = "en_core_web_sm"
