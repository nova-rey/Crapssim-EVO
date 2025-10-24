from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone
from typing import Optional, TextIO

_LOG_FORMAT = "%(asctime)sZ | %(levelname)s | %(name)s | %(message)s"


class _UTCFormatter(logging.Formatter):
    """Formatter that renders timestamps in UTC with a ``Z`` suffix."""

    def converter(self, timestamp: float):  # type: ignore[override]
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).timetuple()

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:  # type: ignore[override,N802]
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")


def setup_logging(
    level: str = "INFO",
    *,
    name: Optional[str] = None,
    stream: Optional[TextIO] = None,
) -> logging.Logger:
    """Configure and return a logger that writes UTC timestamps.

    Args:
        level: Logging level name to apply. Defaults to ``"INFO"``.
        name: Optional logger name. If omitted the root logger is configured.
        stream: Optional IO object to receive log output. Defaults to stdout.
    """

    logger = logging.getLogger(name)
    lvl = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(lvl)

    handler_stream = stream if stream is not None else sys.stdout
    handler = logging.StreamHandler(handler_stream)
    handler.setFormatter(_UTCFormatter(_LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S"))

    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    return logger
