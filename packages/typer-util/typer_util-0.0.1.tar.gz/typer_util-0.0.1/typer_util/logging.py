from __future__ import annotations

import logging

from rich.logging import RichHandler


__all__ = ("cast_logging_level", "default_console_logging")

def cast_logging_level(level: str | int) -> int:
    """Cast a logging level as str or int to int."""
    try:
        return int(level)
    except ValueError:
        level = level.lower()
        if level == "notset":
            return 0
        elif level == "debug":
            return 10
        elif level == "info":
            return 20
        elif level == "warning":
            return 30
        elif level == "error":
            return 40
        elif level == "critical":
            return 50
        else:
            return 0


def default_console_logging(level: str | int = logging.INFO) -> None:
    """Configure console logging for the CLI."""
    level = cast_logging_level(level)
    
    handler = RichHandler()
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)