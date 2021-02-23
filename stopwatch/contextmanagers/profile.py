import functools
import math
from typing import Callable, Optional, Union

from termcolor import colored

from ..statistics import Statistics
from ..stopwatch import Stopwatch
from . import Caller, format_elapsed_time, inspect_caller


def make_report(caller: Caller, name: str, statistics: Statistics) -> str:
    tag = ''.join([colored(f'[{caller.module}', color='blue', attrs=['bold']),
                   colored(f'#{name}', color='green', attrs=['bold']),
                  colored(']', color='blue', attrs=['bold'])])
    items = ', '.join([f'hits={len(statistics)}',
                       f'mean={format_elapsed_time(statistics.mean)}',
                       f'min={format_elapsed_time(statistics.minimum)}',
                       f'median={format_elapsed_time(statistics.median)}',
                       f'max={format_elapsed_time(statistics.maximum)}',
                       f'dev={format_elapsed_time(math.sqrt(statistics.variance))}'])

    return f'{tag} {items}'

def profile(
        func_or_name: Optional[Union[Callable, str]] = None,
        name: Optional[str] = None) -> Callable:
    caller = inspect_caller()

    def decorated(func: Callable):
        nonlocal name
        name = func_or_name if isinstance(func_or_name, str) else name
        if name is None:
            name = func.__name__

        statistics = Statistics()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Stopwatch() as stopwatch:
                result = func(*args, **kwargs)

            statistics.add(stopwatch.elapsed)
            print(make_report(caller, name, statistics))

            return result
        return wrapper
    return decorated(func_or_name) if callable(func_or_name) else decorated