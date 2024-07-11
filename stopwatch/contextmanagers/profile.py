import atexit
import functools
from typing import Callable, Optional

from termcolor import colored

from stopwatch.statistics import Statistics
from stopwatch.stopwatch import Stopwatch
from stopwatch.utils import Caller, inspect_caller


def make_report(caller: Caller, name: str, statistics: Statistics) -> str:
    tag = "".join(
        [
            colored(f"[{caller.module}", color="blue", attrs=["bold"]),
            colored(f"#{name}", color="green", attrs=["bold"]),
            colored("]", color="blue", attrs=["bold"]),
        ]
    )
    return f"{tag} hits={len(statistics)}, {statistics!r}"


def print_report(caller: Caller, name: str, statistics: Statistics):
    if len(statistics) > 0:
        print(make_report(caller, name, statistics))


def profile(func: Optional[Callable] = None, **kwargs) -> Callable:
    caller = inspect_caller()

    def decorated(func: Callable):
        name = kwargs.get("name", func.__name__)
        report_every = kwargs.get("report_every", 1)
        should_report = report_every is not None

        statistics = Statistics()
        atexit.register(print_report, caller, name, statistics)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Stopwatch() as stopwatch:
                result = func(*args, **kwargs)

            statistics.add(stopwatch.elapsed)
            if should_report and (len(statistics) % report_every) == 0:
                print_report(caller, name, statistics)

            return result

        return wrapper

    return decorated(func) if callable(func) else decorated
