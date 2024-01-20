
from __future__ import annotations

from pathlib import Path
from typing import Any, TypeVar, TYPE_CHECKING

from click import ParamType


__all__ = (
    "UseEnvType",
    "UseEnv",
    "EnvOrStr",
    "EnvOrStrParser",
    "EnvOrPath",
    "EnvOrPathParser",
    "EnvOrInt",
    "EnvOrIntParser",
    "EnvOrFloat",
    "EnvOrFloatParser",
)

if TYPE_CHECKING:
    from os import PathLike


class UseEnvType(object):
    """Object where ``None`` is significant. This is a sentinel type like ``None``."""

    def __new__(cls):
        return UseEnv

    def __reduce__(self):
        return (UseEnvType, ())

    def __copy__(self):
        return UseEnv

    def __deepcopy__(self, memo):
        return UseEnv

    def __bool__(self):
        return False

    def __str__(self) -> str:
        return "UseEnv"

    def __repr__(self) -> str:
        return self.__str__()


UseEnv = object.__new__(UseEnvType)


EnvOrStr = TypeVar("EnvOrStr", str, UseEnvType)

class EnvOrStrParser(ParamType):
    name = "EnvOrStr"

    def convert(self, value: str | UseEnvType, *_: Any) -> str | UseEnvType:
        return value


EnvOrPath = TypeVar("EnvOrPath", Path, UseEnvType)

class EnvOrPathParser(ParamType):
    name = "EnvOrPath"

    def convert(self, value: str | PathLike | UseEnvType, *_: Any) -> Path | UseEnvType:
        return value if value is UseEnv else Path(value)


EnvOrInt = TypeVar("EnvOrInt", int, UseEnvType)

class EnvOrIntParser(ParamType):
    name = "EnvOrInt"

    def convert(self, value: str | int | UseEnvType, *_: Any) -> int | UseEnvType:
        return value if value is UseEnv else int(value)


EnvOrFloat = TypeVar("EnvOrFloat", float, UseEnvType)

class EnvOrFloatParser(ParamType):
    name = "EnvOrFloat"

    def convert(self, value: str | float | UseEnvType, *_: Any) -> float | UseEnvType:
        return value if value is UseEnv else float(value)