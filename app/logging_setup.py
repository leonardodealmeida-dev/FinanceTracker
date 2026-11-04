"""Writes errors to a log file (packaged apps have no console).

Location: ~/.financetracker/financetracker.log
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path.home() / ".financetracker"
LOG_FILE = LOG_DIR / "financetracker.log"

logger = logging.getLogger("financetracker")


def setup_logging():
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            LOG_FILE, maxBytes=500_000, backupCount=2, encoding="utf-8"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        logger.addHandler(handler)
    except OSError:
        logger.addHandler(logging.NullHandler())  # never crash on logging
    return logger
