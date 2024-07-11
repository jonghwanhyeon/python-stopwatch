import statistics
from typing import List, Optional

from stopwatch.utils import format_time


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

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        fields = [f"total={format_time(self.total)}"]

        if len(self) > 1:
            fields += [
                f"mean={format_time(self.mean)}",
                f"min={format_time(self.minimum)}",
                f"median={format_time(self.median)}",
                f"max={format_time(self.maximum)}",
            ]

        if len(self) > 2:
            fields += [f"stdev={format_time(self.stdev)}"]

        return ", ".join(fields)
