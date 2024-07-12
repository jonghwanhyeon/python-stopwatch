from typing import Optional

from stopwatch.logger import DefaultLogger, SupportsInfo
from stopwatch.markup import markup
from stopwatch.stopwatch import Stopwatch
from stopwatch.utils import format_time, inspect_caller


# pylint: disable=invalid-name
class stopwatch:
    __slots__ = ("_caller", "_stopwatch", "_message", "_format", "_logger")

    def __init__(
        self,
        message: Optional[str] = None,
        format: str = (
            "[bold][[[blue]{module}[/blue]:[green]{function}[/green]:[yellow]L{line}[/yellow]]][/bold]"
            " ~ "
            "[bold][magenta]{elapsed}[/magenta][/bold]"
            "{message}"
        ),
        logger: Optional[SupportsInfo] = None,
    ):
        self._caller = inspect_caller()
        self._stopwatch = Stopwatch()

        self._message = message
        self._format = markup(format)
        self._logger = logger if logger is not None else DefaultLogger()

    def __enter__(self):
        self._stopwatch.start()

    def __exit__(self, *exception):
        self._stopwatch.stop()
        self._logger.info(self._make_report())

    def _make_report(self) -> str:
        return self._format.format(
            module=self._caller.module,
            function=self._caller.function,
            line=self._caller.line,
            elapsed=format_time(self._stopwatch.elapsed),
            message=f" - {self._message}" if self._message is not None else "",
        )
