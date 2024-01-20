from __future__ import annotations

from typing import Any, TypeVar, TYPE_CHECKING

from pydantic_settings import BaseSettings

from typer_util.types import UseEnv


__all__ = ("Settings",)

if TYPE_CHECKING:
    T = TypeVar("T", bound="Settings")


class Settings(BaseSettings):
    @classmethod
    def settings_load(cls: type[T], **kwargs: Any) -> T:
        """Load environment settings.

        Values passed override environment values. ``typer_utils.UseEnv`` is ignored.
        """
        return cls(**{k: v for k, v in kwargs.items() if v is not UseEnv})