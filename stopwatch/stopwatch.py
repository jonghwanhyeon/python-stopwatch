from __future__ import annotations

import math
import time
from contextlib import contextmanager
from typing import Any, Generator, List, Optional

from .contextmanagers import format_elapsed_time
from .statistics import Statistics


class Lap:
    _running: bool
    _start: float
    _fractions: List[float]

    def __init__(self) -> None:
        self._running = False
        self._start = 0.0
        self._fractions = []

    def start(self) -> None:
        self._running = True
        self._start = time.perf_counter()

    def stop(self) -> None:
        self._fractions.append(time.perf_counter() - self._start)
        self._start = 0.0
        self._running = False

    @property
    def elapsed(self) -> float:
        return ((time.perf_counter() -
                 self._start) if self._running else 0.0) + sum(self._fractions)

    def __repr__(self) -> str:
        return f'Lap(running={self._running}, elapsed={self.elapsed:.4f})'


class Stopwatch:
    _name: Optional[str]
    _laps: List[Lap]
    _lap: Optional[Lap]

    def __init__(self, name: Optional[str] = None) -> None:
        self._name = name
        self.reset()

    def start(self) -> None:
        if self._lap is None:
            self._laps.append(Lap())
            self._lap = self._laps[-1]
            self._lap.start()

    @contextmanager
    def lap(self) -> Generator[None, None, None]:
        # calling start twice consecutively -> use stack to solve this problem
        self.start()
        yield
        self.stop()

    def stop(self) -> None:
        if self._lap is not None:
            self._lap.stop()
            self._lap = None

    def reset(self) -> None:
        self._laps = []
        self._lap = None

    def report(self) -> str:
        statistics = Statistics(values=self.laps)

        items = [f'total={statistics.total:.4f}s']
        if len(statistics) > 1:
            items.extend([
                f'mean={statistics.mean:.4f}s',
                f'min={statistics.minimum:.4f}s',
                f'median={statistics.median:.4f}s',
                f'max={statistics.maximum:.4f}s',
                f'dev={math.sqrt(statistics.variance):.4f}s'
            ])

        return '[Stopwatch{tag}] {statistics}'.format(
            tag=f'#{self.name}' if self.name is not None else '',
            statistics=', '.join(items))

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def laps(self) -> List[float]:
        return [lap.elapsed for lap in self._laps]

    @property
    def elapsed(self) -> float:
        return sum(self.laps)

    def __enter__(self) -> Stopwatch:
        self.start()
        return self

    def __exit__(self, *exception: Any) -> None:
        self.stop()

    def __str__(self) -> str:
        return format_elapsed_time(self.elapsed)

    def __repr__(self) -> str:
        return f'Stopwatch(name={self.name}, elapsed={self.elapsed})'
