from __future__ import annotations

import re
import statistics
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, List, Optional

from stopwatch.utils import format_time


@dataclass(frozen=True)
class Formatter:
    func: Callable[[Statistics], str]
    min_length: int = 1

    def __call__(self, statistics: Statistics) -> str:
        return self.func(statistics)


class Statistics:
    __slots__ = ("_values",)

    def __init__(self, values: Optional[List[float]] = None):
        self._values = [] if values is None else values

    def add(self, value: float):
        self._values.append(value)

    @property
    def mean(self) -> float:
        return statistics.mean(self._values)

    @property
    def maximum(self) -> float:
        return max(self._values)

    @property
    def median(self) -> float:
        return statistics.median(self._values)

    @property
    def minimum(self) -> float:
        return min(self._values)

    @property
    def total(self) -> float:
        return sum(self._values)

    @property
    def variance(self) -> float:
        return statistics.variance(self._values)

    @property
    def stdev(self) -> float:
        return statistics.stdev(self._values)

    _formatters = OrderedDict(
        [
            ("hits", Formatter(lambda self: str(len(self)), min_length=0)),
            ("mean", Formatter(lambda self: format_time(self.mean))),
            ("maximum", Formatter(lambda self: format_time(self.maximum))),
            ("max", Formatter(lambda self: format_time(self.maximum))),
            ("median", Formatter(lambda self: format_time(self.median))),
            ("minimum", Formatter(lambda self: format_time(self.minimum))),
            ("min", Formatter(lambda self: format_time(self.minimum))),
            ("total", Formatter(lambda self: format_time(self.total))),
            ("variance", Formatter(lambda self: format_time(self.variance), min_length=2)),
            ("stdev", Formatter(lambda self: format_time(self.stdev), min_length=2)),
        ]
    )

    def dump(self, fields: Optional[List[str]] = None) -> str:
        if fields is None:
            fields = ["total", "mean", "min", "median", "max", "stdev"]

        items = []
        for field in fields:
            if field not in self._formatters:
                raise ValueError(f"Unknown field {field}")

            formatter = self._formatters[field]
            if len(self) < formatter.min_length:
                continue

            items.append(f"{field}={formatter(self)}")

        return ", ".join(items)

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.dump()})"

    def __str__(self) -> str:
        return self.dump()

    def __format__(self, specifier: str) -> str:
        fields = re.split(r", *", specifier) if specifier else None
        return self.dump(fields)
