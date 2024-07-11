import math
import statistics
from typing import List, Optional


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
        fields = [f"total={self.total:.4f}s"]
        if len(self) > 1:
            fields += [
                f"mean={self.mean:.4f}s",
                f"min={self.minimum:.4f}s",
                f"median={self.median:.4f}s",
                f"max={self.maximum:.4f}s",
                f"stdev={self.stdev:.4f}s",
            ]

        return f"{type(self).__name__}({' ,'.join(fields)})"
