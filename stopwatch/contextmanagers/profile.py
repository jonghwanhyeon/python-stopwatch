import atexit
import functools
import inspect
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Generic, Optional, TypeVar, Union

from typing_extensions import ParamSpec, overload

from stopwatch.logger import DefaultLogger, SupportsInfo
from stopwatch.markup import markup
from stopwatch.statistics import Statistics
from stopwatch.stopwatch import Stopwatch
from stopwatch.utils import Caller, format_time, inspect_caller

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class ProfileArguments(Generic[P, R]):
    func: Optional[Callable[P, R]]
    name: Optional[str]
    report_every: Optional[int]
    format: str
    logger: SupportsInfo

    @classmethod
    def unpack(cls, *args, **kwargs):
        logger = kwargs.get("logger", DefaultLogger())
        report_every = kwargs.get("report_every", 1)
        format = markup(
            kwargs.get(
                "format",
                (
                    "[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold]"
                    " "
                    "{statistics:hits, total, mean, min, median, max, stdev}"
                ),
            )
        )

        if args:
            if callable(args[0]):
                return cls(func=args[0], name=None, report_every=report_every, format=format, logger=logger)
            else:
                return cls(func=None, name=args[0], report_every=report_every, format=format, logger=logger)
        else:
            return cls(func=None, name=None, report_every=report_every, format=format, logger=logger)


@dataclass(frozen=True)
class ProfileContext(Generic[P, R]):
    caller: Caller
    func: Callable[P, R]
    name: Optional[str]
    report_every: Optional[int]
    format: str
    logger: SupportsInfo

    statistics: Statistics = field(default_factory=Statistics)

    def __post_init__(self):
        atexit.register(self.print_report)

    @property
    def should_report(self) -> bool:
        return (self.report_every is not None) and ((len(self.statistics) % self.report_every) == 0)

    def run(self, *args: P.args, **kwargs: P.kwargs):
        with self._record():
            return self.func(*args, **kwargs)

    @contextmanager
    def _record(self):
        with Stopwatch() as stopwatch:
            yield

        self.statistics.add(stopwatch.elapsed)
        if self.should_report:
            self.print_report()

    def _make_report(self) -> str:
        return self.format.format(
            module=self.caller.module,
            name=self.name,
            elapsed=format_time(self.statistics[-1]) if self.statistics else None,
            statistics=self.statistics,
        )

    def print_report(self):
        self.logger.info(self._make_report())


@dataclass(frozen=True)
class AsyncProfileContext(ProfileContext[P, R]):
    func: Callable[P, Coroutine[Any, Any, R]]

    async def run(self, *args: P.args, **kwargs: P.kwargs):
        with self._record():
            return await self.func(*args, **kwargs)


@overload
def profile(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def profile(
    name: Optional[str] = None,
    /,
    report_every: Optional[int] = 1,
    format: str = (
        "[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold]"
        " "
        "{statistics:hits, total, mean, min, median, max, stdev}"
    ),
    logger: Optional[SupportsInfo] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def profile(*args, **kwargs) -> Union[
    Callable[P, R],
    Callable[[Callable[P, R]], Callable[P, R]],
]:
    arguments = ProfileArguments[P, R].unpack(*args, **kwargs)
    caller = inspect_caller()

    def decorated(func: Callable[P, R]) -> Callable[P, R]:
        if not inspect.iscoroutinefunction(func):
            context = ProfileContext[P, R](
                caller=caller,
                func=func,
                name=arguments.name if arguments.name is not None else func.__name__,
                report_every=arguments.report_every,
                format=arguments.format,
                logger=arguments.logger,
            )
        else:
            context = AsyncProfileContext[P, R](
                caller=caller,
                func=func,
                name=arguments.name if arguments.name is not None else func.__name__,
                report_every=arguments.report_every,
                format=arguments.format,
                logger=arguments.logger,
            )

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Union[R, Coroutine[Any, Any, R]]:
            return context.run(*args, **kwargs)

        return wrapper  # type: ignore

    return decorated(arguments.func) if arguments.func is not None else decorated
