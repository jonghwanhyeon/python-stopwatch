import inspect
from dataclasses import dataclass


@dataclass(frozen=True)
class Caller:
    module: str
    function: str
    line: int


def inspect_caller(offset: int = 0) -> Caller:
    stack = inspect.stack()[2 + offset]
    module = inspect.getmodule(stack.frame)

    return Caller(
        module=module.__name__ if module is not None else "Unknown",
        function=stack.function,
        line=stack.lineno,
    )


def format_time(value: float) -> str:
    return f"{value:.4f}s" if value >= 0.1 else f"{value * 1000:.2f}ms"
