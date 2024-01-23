"""Logger"""
import logging
from datetime import datetime
from os.path import (isdir, join as path_join)


def get_logger(logs_dir: str):
    """Return Logger that logs into a new file created at logs_dir"""
    if isdir(logs_dir):
        logs_path = path_join(
            logs_dir,
            f'process_{datetime.now().strftime("%Y%m%d_%H.%M.%S")}.log',
        )
        logging.basicConfig(
            level=logging.INFO,
            filename=logs_path,
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
            encoding="utf-8",
        )
        return logging
    raise ValueError("logs_dir debe ser la ruta a un directorio/carpeta.")
