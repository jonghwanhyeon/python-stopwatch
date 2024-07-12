import time
from contextlib import contextmanager
from typing import List, Optional

from typing_extensions import Self

from stopwatch.statistics import Statistics


class Lap:
    __slots__ = ("_running", "_start", "_fractions")

    def __init__(self):
        self._running = False
        self._start = 0
        self._fractions = []

    def start(self):
        self._running = True
        self._start = time.perf_counter()

    def stop(self):
        self._fractions.append(time.perf_counter() - self._start)
        self._start = 0
        self._running = False

    @property
    def elapsed(self) -> float:
        return ((time.perf_counter() - self._start) if self._running else 0.0) + sum(self._fractions)

    def __repr__(self) -> str:
        return f"Lap(running={self._running}, elapsed={self.elapsed:.4f})"


class Stopwatch:
    __slots__ = ("_name", "_laps", "_lap")

    def __init__(self, name: Optional[str] = None):
        self._name = name
        self.reset()

    def start(self):
        if self._lap is None:
            self._laps.append(Lap())
            self._lap = self._laps[-1]
            self._lap.start()

    @contextmanager
    def lap(self):
        self.start()  # calling start twice consecutively -> use stack to solve this problem
        yield
        self.stop()

    def stop(self):
        if self._lap is not None:
            self._lap.stop()
            self._lap = None

    def reset(self):
        self._laps: List[Lap] = []
        self._lap: Optional[Lap] = None

    def report(self) -> str:
        tag = f"#{self.name}" if self.name is not None else ""
        statistics = Statistics(values=self.laps)
        return f"[Stopwatch{tag}] {statistics.dump()}"

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def laps(self) -> List[float]:
        return [lap.elapsed for lap in self._laps]

    @property
    def elapsed(self) -> float:
        return sum(self.laps)

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, *exception):
        self.stop()
