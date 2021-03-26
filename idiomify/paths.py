from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
ROOT_DIR = LIB_DIR.parent
DATA_DIR = ROOT_DIR.joinpath("data")
DEFS_DIR = DATA_DIR.joinpath("defs")
KEYS_DIR = DATA_DIR.joinpath("keys")


# files - data
IDIOM_ALTS_TSV = DATA_DIR.joinpath("idiom_alts.tsv")  # (idiom, alts list)

# files - defs
URBAN_IDIOM_RAWS_TSV = DEFS_DIR.joinpath("urban_idiom_raw.tsv")  # collection of raw data (idiom, resp)
URBAN_IDIOM_DEFS_TSV = DEFS_DIR.joinpath("urban_idiom_defs.tsv")  # the raw definitions parsed to (idiom, defs)

# files - keys
RAPID_API_TXT = KEYS_DIR.joinpath("rapid_api.txt")
