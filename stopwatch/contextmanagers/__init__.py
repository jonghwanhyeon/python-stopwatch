import inspect
from typing import NamedTuple


class Caller(NamedTuple):
    module: str
    function: str
    line_number: int


def inspect_caller(offset: int = 0) -> Caller:
    stack = inspect.stack()[2 + offset]
    module = inspect.getmodule(stack.frame)
    return Caller(module=module.__name__ if module else '<unknown>',
                  function=stack.function,
                  line_number=stack.lineno)


def format_elapsed_time(elapsed: float) -> str:
    if elapsed >= 0.1:
        return f'{elapsed:.4f}s'
    if elapsed >= 0.01:
        return f'{elapsed * 1e3:.2f}ms'
    if elapsed >= 0.001:
        return f'{elapsed * 1e6:.2f}µs'
    return f'{elapsed * 1e9:.2f}ns'
