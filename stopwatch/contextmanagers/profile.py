import atexit
import functools
import inspect
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, AsyncIterable, Callable, Coroutine, Generic, Iterable, Optional, Tuple, TypeVar, Union

from typing_extensions import ParamSpec, Self, overload

from stopwatch.logger import DefaultLogger, SupportsInfo
from stopwatch.markup import markup
from stopwatch.statistics import Statistics
from stopwatch.stopwatch import Stopwatch
from stopwatch.utils import Caller, format_time, inspect_caller

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class ProfileArguments(Generic[P, R]):
    name: Optional[str]
    report_every: Optional[int]
    report_at_exit: bool
    format: str
    format_at_exit: str
    logger: SupportsInfo

    @classmethod
    def unpack(cls, *args: Union[Callable[P, R], str], **kwargs: Any) -> Tuple[Optional[Callable[P, R]], Self]:
        defaults = {
            "name": None,
            "report_every": 1,
            "report_at_exit": True,
            "format": (
                "[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold]"
                " ~ "
                "[magenta]{elapsed}[/magenta]"
                " - "
                "{statistics:hits, total, mean, min, median, max, stdev}"
            ),
            "format_at_exit": (
                "[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold]"
                " - "
                "{statistics:hits, total, mean, min, median, max, stdev}"
            ),
            "logger": DefaultLogger(),
        }

        arguments = {**defaults, **kwargs}
        arguments["format"] = markup(arguments["format"])
        arguments["format_at_exit"] = markup(arguments["format_at_exit"])

        func = None
        if args:
            if callable(args[0]):
                func = args[0]
            else:
                arguments["name"] = args[0]

        return func, cls(**arguments)


@dataclass
class ProfileContext(ABC, Generic[P, R]):
    caller: Caller
    func: Callable[P, R]
    arguments: ProfileArguments[P, R]

    statistics: Statistics = field(default_factory=Statistics)

    def __post_init__(self):
        if self.arguments.report_at_exit:
            atexit.register(functools.partial(self.print_report, format=self.arguments.format_at_exit))

    @overload
    @abstractmethod
    def build(self) -> Callable[P, R]: ...
    @overload
    @abstractmethod
    def build(self) -> Callable[P, Iterable[R]]: ...

    @overload
    @abstractmethod
    async def build(self) -> Callable[P, Coroutine[Any, Any, R]]: ...

    @overload
    @abstractmethod
    async def build(self) -> Callable[P, AsyncIterable[R]]: ...

    @property
    def should_report(self) -> bool:
        return (self.arguments.report_every is not None) and ((len(self.statistics) % self.arguments.report_every) == 0)

    def print_report(self, format: str):
        self.arguments.logger.info(self._make_report(format))

    @contextmanager
    def _record(self):
        with Stopwatch() as stopwatch:
            yield

        self.statistics.add(stopwatch.elapsed)
        if self.should_report:
            self.print_report(self.arguments.format)

    def _make_report(self, format: str) -> str:
        return format.format(
            module=self.caller.module,
            name=self.arguments.name,
            elapsed=format_time(self.statistics[-1]) if self.statistics else None,
            statistics=self.statistics,
        )


@dataclass
class FunctionProfileContext(ProfileContext[P, R]):
    func: Callable[P, R]

    def build(self) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with self._record():
                return self.func(*args, **kwargs)

        return wrapper


@dataclass
class GeneratorFunctionProfileContext(ProfileContext[P, R]):
    func: Callable[P, Iterable[R]]

    def build(self) -> Callable[P, Iterable[R]]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Iterable[R]:
            with self._record():
                yield from self.func(*args, **kwargs)

        return wrapper


@dataclass
class AsyncFunctionProfileContext(ProfileContext[P, R]):
    func: Callable[P, Coroutine[Any, Any, R]]

    def build(self) -> Callable[P, Coroutine[Any, Any, R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with self._record():
                return await self.func(*args, **kwargs)

        return wrapper


@dataclass
class AsyncGeneratorFunctionProfileContext(ProfileContext[P, R]):
    func: Callable[P, AsyncIterable[R]]

    def build(self) -> Callable[P, AsyncIterable[R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> AsyncIterable[R]:
            with self._record():
                async for value in self.func(*args, **kwargs):
                    yield value

        return wrapper


@overload
def profile(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def profile(
    name: Optional[str] = None,
    /,
    report_every: Optional[int] = 1,
    report_at_exit: bool = True,
    format: str = (
        "[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold]"
        " ~ "
        "[magenta]{elapsed}[/magenta]"
        " - "
        "{statistics:hits, total, mean, min, median, max, stdev}"
    ),
    format_at_exit: str = (
        "[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold]"
        " - "
        "{statistics:hits, total, mean, min, median, max, stdev}"
    ),
    logger: Optional[SupportsInfo] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def profile(*args, **kwargs) -> Union[
    Callable[P, R],
    Callable[[Callable[P, R]], Callable[P, R]],
]:
    func, arguments = ProfileArguments[P, R].unpack(*args, **kwargs)
    caller = inspect_caller()

    def decorated(func: Callable[P, R]) -> Callable[P, R]:
        if arguments.name is None:
            arguments.name = func.__name__

        if inspect.isasyncgenfunction(func):
            context = AsyncGeneratorFunctionProfileContext[P, R](caller=caller, func=func, arguments=arguments)
        elif inspect.iscoroutinefunction(func):
            context = AsyncFunctionProfileContext[P, R](caller=caller, func=func, arguments=arguments)
        elif inspect.isgeneratorfunction(func):
            context = GeneratorFunctionProfileContext[P, R](caller=caller, func=func, arguments=arguments)
        else:
            context = FunctionProfileContext[P, R](caller=caller, func=func, arguments=arguments)

        return functools.update_wrapper(context.build(), func)  # type:ignore

    return decorated(func) if func is not None else decorated
