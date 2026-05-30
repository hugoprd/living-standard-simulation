import sys
from pathlib import Path
import time

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from loguru import logger  # noqa: E402
from logs.set_logger import setup_logger  # noqa: E402

LOG_FILE = ROOT_DIR / "logs"
LOG_NAME = "data_log"

setup_logger(log_file_path=LOG_FILE, log_name=LOG_NAME, overwrite=True)


def time_count(func):
    """
    Measures execution time.
    """

    def wrap(*args, **kwargs):
        pre_run = time.time()
        result = func(*args, **kwargs)
        post_run = time.time()

        logger.info(f"{func.__name__} ran in {(post_run - pre_run):.6f} seconds.")

        return result

    return wrap
