import inspect
from collections import namedtuple

Caller = namedtuple("Caller", ["module", "function", "line_number"])


def format_time(value: float) -> str:
    return f"{value:.4f}s" if value >= 0.1 else f"{value * 1000:.2f}ms"


def inspect_caller(offset: int = 0) -> Caller:
    stack = inspect.stack()[2 + offset]
    return Caller(module=inspect.getmodule(stack.frame).__name__, function=stack.function, line_number=stack.lineno)
