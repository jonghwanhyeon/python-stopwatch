from typing import Optional

from termcolor import colored

from stopwatch.logger import DefaultLogger, SupportsInfo
from stopwatch.stopwatch import Stopwatch
from stopwatch.utils import format_time, inspect_caller


# pylint: disable=invalid-name
class stopwatch:
    __slots__ = ("_caller", "_stopwatch", "_message", "_logger")

    def __init__(self, message: Optional[str] = None, logger: Optional[SupportsInfo] = None):
        self._caller = inspect_caller()
        self._stopwatch = Stopwatch()

        self._message = message
        self._logger = logger if logger is not None else DefaultLogger()

    def __enter__(self):
        self._stopwatch.start()

    def __exit__(self, *exception):
        self._stopwatch.stop()
        self._logger.info(self._make_report())

    def _make_report(self) -> str:
        items = [
            colored("[", attrs=["bold"]),
            colored(self._caller.module, color="blue", attrs=["bold"]),
            colored(":", attrs=["bold"]),
            colored(self._caller.function, color="green", attrs=["bold"]),
            colored(":", attrs=["bold"]),
            colored(f"L{self._caller.line}", color="yellow", attrs=["bold"]),
            colored("]", attrs=["bold"]),
            " ~ ",
            colored(format_time(self._stopwatch.elapsed), color="magenta", attrs=["bold"]),
        ]

        if self._message is not None:
            items += [" - ", self._message]

        return "".join(items)
