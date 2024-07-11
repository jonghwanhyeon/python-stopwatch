import sys
from typing import Any, TextIO

from typing_extensions import Protocol


class SupportsInfo(Protocol):
    def info(self, *args: Any, **kwargs: Any): ...


class DefaultLogger:
    __slots__ = ("_file",)

    def __init__(self, file: TextIO = sys.stderr):
        self._file = file

    def info(self, message: str):
        print(message, file=self._file)
