from __future__ import annotations
import logging
import sys
from datetime import datetime, timezone
from typing import Optional

_LOG_FORMAT = "%(asctime)sZ | %(levelname)s | %(name)s | %(message)s"

class _UTCFormatter(logging.Formatter):
    """Formatter that renders timestamps in UTC ISO-8601 format."""
    def formatTime(self, record, datefmt=None):
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

def setup_logging(level: str = "INFO", name: Optional[str] = None) -> logging.Logger:
    """
    Configure a console logger with UTC timestamps and idempotent handlers.
    Returns the configured logger (root by default).
    """
    lvl = getattr(logging, str(level).upper(), logging.INFO)
    logger = logging.getLogger(name) if name else logging.getLogger()

    # Prevent duplicate EVO handlers
    needs_handler = True
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler) and getattr(h, "_evo_handler", False):
            needs_handler = False
            break

    logger.setLevel(lvl)
    if needs_handler:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(lvl)
        handler.setFormatter(_UTCFormatter(_LOG_FORMAT))
        handler._evo_handler = True  # mark as EVO handler
        logger.addHandler(handler)

    return logger
