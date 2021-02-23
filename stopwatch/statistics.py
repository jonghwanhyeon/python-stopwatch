import statistics
from typing import List, Optional


class Statistics:
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
        return statistics.pvariance(self._values)

    def __len__(self) -> int:
        return len(self._values)