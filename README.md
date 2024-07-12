# Stopwatch

A simple stopwatch for measuring code performance.

## Installing

To install the library, you can just run the following command:

```shell
$ python3 -m pip install python-stopwatch
```

## Examples

```python
import time
from stopwatch import Stopwatch, profile

stopwatch = Stopwatch()
stopwatch.start()
time.sleep(3.0)
stopwatch.stop()
print(stopwatch.elapsed)
# 3.003047182224691

with Stopwatch(name="outer") as outer_stopwatch:
    with Stopwatch(name="inner") as inner_stopwatch:
        for i in range(5):
            with inner_stopwatch.lap():
                time.sleep(i / 10)
print(inner_stopwatch.elapsed)
# 1.0013675531372428
print(inner_stopwatch.laps)
# [5.3666066378355026e-05, 0.10502862487919629, 0.202481625135988, 0.30503024999052286, 0.4007756249047816]
print(outer_stopwatch.report())
# [Stopwatch#outer] total=1.0135s, mean=1.0135s, min=1.0135s, median=1.0135s, max=1.0135s
print(inner_stopwatch.report())
# [Stopwatch#inner] total=1.0134s, mean=0.2027s, min=0.05ms, median=0.2025s, max=0.4008s, stdev=0.1584s
```

```python
import time
from stopwatch import profile

@profile
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__:wait_for] hits=1, total=0.00ms, mean=0.00ms, min=0.00ms, median=0.00ms, max=0.00ms
# [__main__:wait_for] hits=2, total=0.5015s, mean=0.2508s, min=0.00ms, median=0.2508s, max=0.5015s, stdev=0.3546s
# [__main__:wait_for] hits=3, total=1.4050s, mean=0.4683s, min=0.00ms, median=0.5015s, max=0.9034s, stdev=0.4526s
# [__main__:wait_for] hits=4, total=2.6110s, mean=0.6528s, min=0.00ms, median=0.7025s, max=1.2060s, stdev=0.5222s
# [__main__:wait_for] hits=5, total=4.0223s, mean=0.8045s, min=0.00ms, median=0.9034s, max=1.4113s, stdev=0.5653s
# [__main__:wait_for] hits=6, total=5.5354s, mean=0.9226s, min=0.00ms, median=1.0547s, max=1.5131s, stdev=0.5825s
# [__main__:wait_for] hits=6, total=5.5354s, mean=0.9226s, min=0.00ms, median=1.0547s, max=1.5131s, stdev=0.5825s
```

```python
import time
from stopwatch import profile

@profile("wait for ts")
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__:wait for ts] hits=1, total=0.00ms, mean=0.00ms, min=0.00ms, median=0.00ms, max=0.00ms
# [__main__:wait for ts] hits=2, total=0.5041s, mean=0.2520s, min=0.00ms, median=0.2520s, max=0.5041s, stdev=0.3564s
# [__main__:wait for ts] hits=3, total=1.4133s, mean=0.4711s, min=0.00ms, median=0.5041s, max=0.9093s, stdev=0.4555s
# [__main__:wait for ts] hits=4, total=2.6385s, mean=0.6596s, min=0.00ms, median=0.7067s, max=1.2252s, stdev=0.5296s
# [__main__:wait for ts] hits=5, total=4.0690s, mean=0.8138s, min=0.00ms, median=0.9093s, max=1.4305s, stdev=0.5738s
# [__main__:wait for ts] hits=6, total=5.6026s, mean=0.9338s, min=0.00ms, median=1.0672s, max=1.5336s, stdev=0.5914s
# [__main__:wait for ts] hits=6, total=5.6026s, mean=0.9338s, min=0.00ms, median=1.0672s, max=1.5336s, stdev=0.5914s
```

```python
import time
from stopwatch import profile

@profile("wait for ts", report_every=2)
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__:wait for ts] hits=2, total=0.5034s, mean=0.2517s, min=0.02ms, median=0.2517s, max=0.5034s, stdev=0.3559s
# [__main__:wait for ts] hits=4, total=2.6276s, mean=0.6569s, min=0.02ms, median=0.7065s, max=1.2146s, stdev=0.5260s
# [__main__:wait for ts] hits=6, total=5.5693s, mean=0.9282s, min=0.02ms, median=1.0621s, max=1.5221s, stdev=0.5863s
# [__main__:wait for ts] hits=6, total=5.5693s, mean=0.9282s, min=0.02ms, median=1.0621s, max=1.5221s, stdev=0.5863s
```

```python
import time
from stopwatch import profile

@profile("wait for ts", report_every=None)
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__:wait for ts] hits=6, total=5.5361s, mean=0.9227s, min=0.00ms, median=1.0554s, max=1.5145s, stdev=0.5827s
```

```python
import time
from stopwatch import profile

@profile(
    "wait for ts",
    format="[bold][[[blue]{module}[/blue]:[green]{name}[/green]]][/bold] {statistics:hits, mean, median, stdev}",
)
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__:wait for ts] hits=1, mean=0.01ms, median=0.01ms
# [__main__:wait for ts] hits=2, mean=0.2527s, median=0.2527s, stdev=0.3573s
# [__main__:wait for ts] hits=3, mean=0.4720s, median=0.5053s, stdev=0.4562s
# [__main__:wait for ts] hits=4, mean=0.6579s, median=0.7079s, stdev=0.5263s
# [__main__:wait for ts] hits=5, mean=0.8096s, median=0.9105s, stdev=0.5682s
# [__main__:wait for ts] hits=6, mean=0.9282s, median=1.0631s, stdev=0.5854s
# [__main__:wait for ts] hits=6, mean=0.9282s, median=1.0631s, stdev=0.5854s
```

```python
import time
from stopwatch import stopwatch

with stopwatch():
    for i in range(5):
        time.sleep(i / 10)
# [__main__:<module>:L5] ~ 1.0013s


with stopwatch("with message"):
    for i in range(5):
        time.sleep(i / 10)
# [__main__:<module>:L11] ~ 1.0013s - with message
```
