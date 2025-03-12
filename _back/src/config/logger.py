import os
import sys
from pathlib import Path

from loguru import logger

from config.settings import SETTINGS


def setup_logger():
    # Configure log format with colors
    log_format = "<level>{level: >6}</level> | {time:MM-DD HH:mm:ss} | ({line}) {file.name} || {message}"

    # Remove default handler
    logger.remove()

    # Add console handler with colors enabled
    logger.add(sys.stderr, format=log_format, level="DEBUG", colorize=True)

    # Add file handler for production environment (no colors for file logs)
    if SETTINGS.ENV == "prod":
        logger.add(
            os.path.join(Path(".").parent.parent / "logs", "uxer_back.log"),
            format=log_format,
            level="DEBUG",
            rotation="50 MB",
            retention=3,
            colorize=False,
        )

    return logger
