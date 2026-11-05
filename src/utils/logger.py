"""Logging setup — file + console."""

import logging
from pathlib import Path
from .config import config, ROOT


def setup_logger(name: str = "bahoush_bot") -> logging.Logger:
    """Configure and return a logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    # Format
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    # File
    log_path = ROOT / config.LOG_FILE
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger


log = setup_logger()
