"""
Application logging configuration.

Provides a centralized logger for the entire project.

Usage
-----

from app.core.logger import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Information")
logger.warning("Warning")
logger.error("Error")
logger.exception("Exception occurred")
"""

import logging
import os
import sys


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------
# Configure Root Logger
# ---------------------------------------------------------

logging.basicConfig(
    level=getattr(
        logging,
        LOG_LEVEL,
        logging.INFO,
    ),
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    force=True,
)


# ---------------------------------------------------------
# Logger Factory
# ---------------------------------------------------------

def get_logger(
    name: str,
) -> logging.Logger:
    """
    Return a configured logger.

    Parameters
    ----------
    name : str
        Usually __name__.

    Returns
    -------
    logging.Logger
    """

    return logging.getLogger(name)