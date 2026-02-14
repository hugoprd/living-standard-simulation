# logs/set_logger.py
from loguru import logger
from pathlib import Path


def setup_logger(log_file_path: Path):
    logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        rotation="10 MB",  # evita que o txt fique infinito
    )
