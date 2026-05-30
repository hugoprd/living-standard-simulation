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
logger.info("LOG INITIALIZED.")
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

    if not dfs:
        logger.error("No processed files found. Aborting.")
        return

    logger.info("Starting the Grand Merge for the Refined layer...")

    dataframes = list(dfs.values())

    df_final = reduce(lambda left, right: pd.merge(left, right, on=["municipio", "ano"], how="outer"), dataframes)

    df_final = df_final.sort_values(by=["municipio", "ano"]).reset_index(drop=True)

    REFINED_PATH.mkdir(parents=True, exist_ok=True)

    csv_file = REFINED_PATH / "master_living_standard.csv"
    df_final.to_csv(csv_file, sep=";", encoding="utf-8", index=False)
    logger.info(f"Table consolidated and saved as CSV: {csv_file.name}")

    parquet_file = REFINED_PATH / "master_living_standard.parquet"
    try:
        df_final.to_parquet(parquet_file, index=False)
        logger.info(f"Table consolidated and saved as Parquet: {parquet_file.name}")
    except ImportError:
        logger.warning(
            "Parquet file was not saved. You need the engine installed. "
            "Run 'conda install pyarrow' or 'pip install pyarrow' to enable it."
        )

    logger.info(f"Pipeline finished! The final dataset shape is {df_final.shape[0]} rows and {df_final.shape[1]} columns.")


if __name__ == "__main__":
    build_final_data()
