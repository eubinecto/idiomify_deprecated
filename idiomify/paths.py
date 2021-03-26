from pathlib import Path

# directories
LIB_DIR = Path(__file__).resolve().parent
ROOT_DIR = LIB_DIR.parent
DATA_DIR = ROOT_DIR.joinpath("data")
DEFS_DIR = DATA_DIR.joinpath("defs"
                             )
# files
IDIOM_ALTS_TSV = DATA_DIR.joinpath("idiom_alts.tsv")  # (idiom, alts list)
URBAN_DEFS_RAW_TSV = DEFS_DIR.joinpath("urban_defs_raw.tsv")  # collection of raw data (idiom, resp)
URBAN_DEFS_TSV = DEFS_DIR.joinpath("urban_defs.tsv")  # the raw definitions parsed to (idiom, defs)
# and so on. (wiktionary, phrases, etc)
