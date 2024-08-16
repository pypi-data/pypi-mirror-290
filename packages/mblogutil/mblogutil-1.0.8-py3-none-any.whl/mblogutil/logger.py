from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

import mblogutil

LOG_LEVEL_MAPPING = logging.getLevelNamesMapping()

def _get_log_fullpath(log_path: str, log_name: str):
    log_filename = f"{log_name}.{_get_timestamp()}.log"
    log_actual = os.path.join(log_path, log_filename)
    return log_actual

def _get_timestamp() -> str:
    current_dtm = datetime.now()
    return current_dtm.strftime("%Y%m%d.%H%M%S")

def get(logger_name: str, log_level: str = "INFO", log_path: str = "logs", rotating: bool = False, maxBytes: int | None = None, backupCount: int | None = None) -> logging.Logger:
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    upper_log_level = log_level.upper()
    
    if upper_log_level not in LOG_LEVEL_MAPPING.keys():
        raise ValueError(f"{upper_log_level} not in {[str(key) for key in LOG_LEVEL_MAPPING.keys()]}")
    
    real_log_level = LOG_LEVEL_MAPPING[log_level.upper()]

    logger = logging.getLogger(logger_name)
    logger.setLevel(real_log_level)

    log_full_path = _get_log_fullpath(log_path, logger_name)

    if mblogutil.ROTATING or rotating:
        max_bytes = maxBytes if maxBytes is not None else mblogutil.MAXBYTES
        backup_count = backupCount if backupCount is not None else mblogutil.BACKUPCOUNT
        file_handler = RotatingFileHandler(filename=log_full_path, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(real_log_level)
    else:
        file_handler = logging.FileHandler(filename=log_full_path)
        file_handler.setLevel(real_log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(real_log_level)

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger