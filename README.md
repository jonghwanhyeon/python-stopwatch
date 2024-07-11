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
# [3.256136551499367e-05, 0.10015189787372947, 0.20030939625576138, 0.3003752687945962, 0.40049842884764075]
print(outer_stopwatch.report())
# [Stopwatch#outer] total=1.0015s
print(inner_stopwatch.report())
# [Stopwatch#inner] total=1.0014s, mean=0.2003s, min=0.0000s, median=0.2003s, max=0.4005s, dev=0.1416s
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
# [__main__:wait_for] hits=1, total=0.00ms
# [__main__:wait_for] hits=2, total=0.5052s, mean=0.2526s, min=0.00ms, median=0.2526s, max=0.5052s
# [__main__:wait_for] hits=3, total=1.4137s, mean=0.4712s, min=0.00ms, median=0.5052s, max=0.9085s, stdev=0.4552s
# [__main__:wait_for] hits=4, total=2.6274s, mean=0.6568s, min=0.00ms, median=0.7069s, max=1.2137s, stdev=0.5253s
# [__main__:wait_for] hits=5, total=4.0444s, mean=0.8089s, min=0.00ms, median=0.9085s, max=1.4170s, stdev=0.5679s
# [__main__:wait_for] hits=6, total=5.5655s, mean=0.9276s, min=0.00ms, median=1.0611s, max=1.5210s, stdev=0.5853s
# [__main__:wait_for] hits=6, total=5.5655s, mean=0.9276s, min=0.00ms, median=1.0611s, max=1.5210s, stdev=0.5853s
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
# [__main__:wait for ts] hits=1, total=0.01ms
# [__main__:wait for ts] hits=2, total=0.5053s, mean=0.2526s, min=0.01ms, median=0.2526s, max=0.5053s
# [__main__:wait for ts] hits=3, total=1.4123s, mean=0.4708s, min=0.01ms, median=0.5053s, max=0.9070s, stdev=0.4545s
# [__main__:wait for ts] hits=4, total=2.6228s, mean=0.6557s, min=0.01ms, median=0.7062s, max=1.2105s, stdev=0.5239s
# [__main__:wait for ts] hits=5, total=4.0385s, mean=0.8077s, min=0.01ms, median=0.9070s, max=1.4157s, stdev=0.5669s
# [__main__:wait for ts] hits=6, total=5.5588s, mean=0.9265s, min=0.01ms, median=1.0587s, max=1.5203s, stdev=0.5846s
# [__main__:wait for ts] hits=6, total=5.5588s, mean=0.9265s, min=0.01ms, median=1.0587s, max=1.5203s, stdev=0.5846s
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
# [__main__:wait for ts] hits=2, total=0.5025s, mean=0.2512s, min=0.02ms, median=0.2512s, max=0.5025s
# [__main__:wait for ts] hits=4, total=2.6232s, mean=0.6558s, min=0.02ms, median=0.7052s, max=1.2129s, stdev=0.5252s
# [__main__:wait for ts] hits=6, total=5.5613s, mean=0.9269s, min=0.02ms, median=1.0604s, max=1.5216s, stdev=0.5856s
# [__main__:wait for ts] hits=6, total=5.5613s, mean=0.9269s, min=0.02ms, median=1.0604s, max=1.5216s, stdev=0.5856s
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
#[__main__:wait for ts] hits=6, total=5.5521s, mean=0.9254s, min=0.02ms, median=1.0573s, max=1.5189s, stdev=0.5842s
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
