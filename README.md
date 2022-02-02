# Stopwatch

A simple stopwatch for measuring code performance.

## Installing

To install the library, you can just run the following command:

```shell
# Linux/macOS
python3 -m pip install python-stopwatch

# Windows
py -3 -m pip install python-stopwatch
```

To install the development version, do the following:

```shell
git clone https://github.com/jonghwanhyeon/python-stopwatch
cd python-stopwatch
python3 -m pip install .
```

## Examples

```python
import time
from stopwatch import Stopwatch, profile

stopwatch = Stopwatch()
stopwatch.start()
time.sleep(3.0)
stopwatch.stop()
print(stopwatch.elapsed) # 3.003047182224691

with Stopwatch(name='outer') as outer_stopwatch:
    with Stopwatch(name='inner') as inner_stopwatch:
        for i in range(5):
            with inner_stopwatch.lap():
                time.sleep(i / 10)
print(inner_stopwatch.elapsed) # 1.0013675531372428
print(inner_stopwatch.laps) # [3.256136551499367e-05, 0.10015189787372947, 0.20030939625576138, 0.3003752687945962, 0.40049842884764075]
print(outer_stopwatch.report()) # [Stopwatch#outer] total=1.0015s
print(inner_stopwatch.report()) # [Stopwatch#inner] total=1.0014s, mean=0.2003s, min=0.0000s, median=0.2003s, max=0.4005s, dev=0.1416s


@profile
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__#wait_for] hits=1, mean=0.02ms, min=0.02ms, median=0.02ms, max=0.02ms, dev=0.00ms
# [__main__#wait_for] hits=2, mean=0.2507s, min=0.02ms, median=0.2507s, max=0.5014s, dev=0.2507s
# [__main__#wait_for] hits=3, mean=0.4680s, min=0.02ms, median=0.5014s, max=0.9026s, dev=0.3692s
# [__main__#wait_for] hits=4, mean=0.6519s, min=0.02ms, median=0.7020s, max=1.2036s, dev=0.4513s
# [__main__#wait_for] hits=5, mean=0.8024s, min=0.02ms, median=0.9026s, max=1.4046s, dev=0.5036s
# [__main__#wait_for] hits=6, mean=0.9196s, min=0.02ms, median=1.0531s, max=1.5055s, dev=0.5291s
# [__main__#wait_for] hits=6, mean=0.9196s, min=0.02ms, median=1.0531s, max=1.5055s, dev=0.5291s


@profile(name='wait for ts')
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__#wait for ts] hits=1, mean=0.01ms, min=0.01ms, median=0.01ms, max=0.01ms, dev=0.00ms
# [__main__#wait for ts] hits=2, mean=0.2505s, min=0.01ms, median=0.2505s, max=0.5009s, dev=0.2505s
# [__main__#wait for ts] hits=3, mean=0.4675s, min=0.01ms, median=0.5009s, max=0.9017s, dev=0.3689s
# [__main__#wait for ts] hits=4, mean=0.6513s, min=0.01ms, median=0.7013s, max=1.2024s, dev=0.4509s
# [__main__#wait for ts] hits=5, mean=0.8016s, min=0.01ms, median=0.9017s, max=1.4031s, dev=0.5031s
# [__main__#wait for ts] hits=6, mean=0.9186s, min=0.01ms, median=1.0521s, max=1.5037s, dev=0.5286s
# [__main__#wait for ts] hits=6, mean=0.9186s, min=0.01ms, median=1.0521s, max=1.5037s, dev=0.5286s



@profile(name='wait for ts', report_every=2)
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__#wait for ts] hits=2, mean=0.2504s, min=0.01ms, median=0.2504s, max=0.5007s, dev=0.2503s
# [__main__#wait for ts] hits=4, mean=0.6513s, min=0.01ms, median=0.7014s, max=1.2025s, dev=0.4510s
# [__main__#wait for ts] hits=6, mean=0.9188s, min=0.01ms, median=1.0523s, max=1.5039s, dev=0.5287s
# [__main__#wait for ts] hits=6, mean=0.9176s, min=0.01ms, median=1.0510s, max=1.5018s, dev=0.5279s


@profile(name='wait for ts', report_every=None)
def wait_for(ts):
    if not ts:
        return

    time.sleep(ts[0])
    wait_for(ts[1:])

wait_for([0.1, 0.2, 0.3, 0.4, 0.5])
# [__main__#wait for ts] hits=6, mean=0.9188s, min=0.01ms, median=1.0523s, max=1.5039s, dev=0.5287s


with stopwatch():
    for i in range(5):
        time.sleep(i / 10)
# [__main__:<module>:1] ~ 1.0013s


with stopwatch('with message'):
    for i in range(5):
        time.sleep(i / 10)
# [__main__:<module>:1] ~ 1.0013s - with message
```
