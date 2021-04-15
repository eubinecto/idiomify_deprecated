from os import path

# directories
HOME_DIR = path.expanduser("~")
DATA_DIR = path.join(HOME_DIR, 'data')
CORPORA_DIR = path.join(HOME_DIR, "corpora")  # this is always at home.
PROJECT_DATA_DIR = path.join(DATA_DIR, "data_idiomify")
IDIOM2VEC_DIR = path.join(PROJECT_DATA_DIR, "idiom2vec")

# idiom2vec
IDIOM2VEC_WV_001_BIN = path.join(IDIOM2VEC_DIR, "idiom2vec_wv_001.bin")
IDIOM2VEC_DV_001_BIN = path.join(IDIOM2VEC_DIR, "idiom2vec_dv_001.bin")

# spacy
NLP_MODEL = "en_core_web_sm"
