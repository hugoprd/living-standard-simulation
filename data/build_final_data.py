import sys
from pathlib import Path
from functools import reduce

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from utils.time_utils import time_count  # noqa: E402

from loguru import logger  # noqa: E402
from logs.set_logger import setup_logger  # noqa: E402

import pandas as pd  # noqa: E402
from pandas import DataFrame  # noqa: E402

# ===== LOG ===== #
LOG_FILE = ROOT_DIR / "logs"
LOG_NAME = "data_log"

setup_logger(log_file_path=LOG_FILE, log_name=LOG_NAME, overwrite=True)

logger.info("=" * 32)
logger.info("LOG INICIALIZED.")
###################

DATA_PATH = ROOT_DIR / "data/processed"
REFINED_PATH = ROOT_DIR / "data/refined"


def load_data() -> dict[DataFrame]:
    dfs = {}

    for file in DATA_PATH.rglob("*.csv"):
        file_type = file.stem.split("_")[0].upper()

        df = pd.read_csv(file, sep=";", encoding="utf-8")

        dfs[file_type] = df
        logger.info(f"Loaded '{file_type}' with shape {df.shape}")

    return dfs


@time_count
def build_final_data():
    dfs = load_data()


if __name__ == "__main__":
    build_final_data()
