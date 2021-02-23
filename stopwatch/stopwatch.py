import math
import time
from contextlib import contextmanager
from typing import List, Optional

from .statistics import Statistics


class Lap:
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
        return ((time.perf_counter() - self._start) if self._running else 0.0) \
               + sum(self._fractions)

    def __repr__(self) -> str:
        return f'Lap(running={self._running}, elapsed={self.elapsed:.4f})'


class Stopwatch:
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
        self.start() # calling start twice consecutively -> use stack to solve this problem
        yield
        self.stop()

    def stop(self):
        if self._lap is not None:
            self._lap.stop()
            self._lap = None

    def reset(self):
        self._laps: List[Lap] = []
        self._lap: Optional[Lap] = None

    def report(self):
        statistics = Statistics(values=self.laps)

        items = [f'total={statistics.total:.4f}s']
        if len(statistics) > 1:
            items.extend([f'mean={statistics.mean:.4f}s',
                          f'min={statistics.minimum:.4f}s',
                          f'median={statistics.median:.4f}s',
                          f'max={statistics.maximum:.4f}s',
                          f'dev={math.sqrt(statistics.variance):.4f}s'])

        return '[Stopwatch{tag}] {statistics}'.format(
            tag=f'#{self.name}' if self.name is not None else '',
            statistics=', '.join(items))

    @property
    def name(self) -> str:
        return self._name

    @property
    def laps(self) -> List[float]:
        return [lap.elapsed for lap in self._laps]

    @property
    def elapsed(self) -> float:
        return sum(self.laps)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop()