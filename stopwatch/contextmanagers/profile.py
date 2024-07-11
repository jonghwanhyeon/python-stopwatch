import atexit
import functools
from dataclasses import dataclass, field
from typing import Callable, Generic, Optional, TypeVar, Union

from termcolor import colored
from typing_extensions import ParamSpec, overload

from stopwatch.logger import DefaultLogger, SupportsInfo
from stopwatch.statistics import Statistics
from stopwatch.stopwatch import Stopwatch
from stopwatch.utils import Caller, inspect_caller

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class ProfileArguments(Generic[P, R]):
    func: Optional[Callable[P, R]]
    name: Optional[str]
    report_every: Optional[int]
    logger: SupportsInfo

    @classmethod
    def unpack(cls, *args, **kwargs):
        logger = kwargs.get("logger", DefaultLogger())
        report_every = kwargs.get("report_every", 1)

        if args:
            if callable(args[0]):
                return cls(func=args[0], name=None, report_every=report_every, logger=logger)
            else:
                return cls(func=None, name=args[0], report_every=report_every, logger=logger)
        else:
            return cls(func=None, name=None, report_every=report_every, logger=logger)


@dataclass
class ProfileContext:
    caller: Caller
    name: Optional[str]
    report_every: Optional[int]
    logger: SupportsInfo

    statistics: Statistics = field(default_factory=Statistics)

    @property
    def should_report(self) -> bool:
        return (self.report_every is not None) and ((len(self.statistics) % self.report_every) == 0)

    def _make_report(self) -> str:
        prefix = "".join(
            [
                colored(f"[", attrs=["bold"]),
                colored(f"{self.caller.module}", color="blue", attrs=["bold"]),
                colored(f":", attrs=["bold"]),
                colored(self.name, color="green", attrs=["bold"]),
                colored("]", attrs=["bold"]),
            ]
        )
        return f"{prefix} hits={len(self.statistics)}, {self.statistics!r}"

    def print_report(self):
        self.logger.info(self._make_report())


@overload
def profile(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def profile(
    name: Optional[str] = None,
    /,
    report_every: Optional[int] = 1,
    logger: Optional[SupportsInfo] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def profile(*args, **kwargs) -> Union[
    Callable[P, R],
    Callable[[Callable[P, R]], Callable[P, R]],
]:
    arguments = ProfileArguments[P, R].unpack(*args, **kwargs)
    caller = inspect_caller()

    def decorated(func: Callable[P, R]) -> Callable[P, R]:
        context = ProfileContext(
            caller=caller,
            name=arguments.name if arguments.name is not None else func.__name__,
            report_every=arguments.report_every,
            logger=arguments.logger,
        )

        atexit.register(context.print_report)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with Stopwatch() as stopwatch:
                result = func(*args, **kwargs)

            context.statistics.add(stopwatch.elapsed)
            if context.should_report:
                context.print_report()

            return result

        return wrapper

    return decorated(arguments.func) if arguments.func is not None else decorated
