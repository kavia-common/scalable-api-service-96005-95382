import logging
import os


def configure_logging() -> None:
    """
    Configure app-wide logging level and format.
    """
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    # Fallback to INFO if invalid level provided
    log_level = getattr(logging, level, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
