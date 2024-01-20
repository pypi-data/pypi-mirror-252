from __future__ import annotations

from typing import Any

from rich import print
from rich.panel import Panel
from typer import Exit
from typer.rich_utils import (
    highlighter,
    ALIGN_ERRORS_PANEL,
    ERRORS_PANEL_TITLE,
    STYLE_ERRORS_PANEL_BORDER,
)


__all__ = ("exit_with_error", "exit_with_success")


def exit_with_error(message: str, code: int = 1) -> None:
    """Utility to print a stylized error message and exit with a non-zero code."""
    print(
        Panel(
            highlighter(message),
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title=ERRORS_PANEL_TITLE,
            title_align=ALIGN_ERRORS_PANEL,
        )
    )
    raise Exit(code)


def exit_with_success(message: str, **kwargs: Any) -> None:
    """Utility to print a stylized success message and exit with a zero code."""
    kwargs.setdefault("style", "green")
    print(f"[green]{message}")
    raise Exit(0)