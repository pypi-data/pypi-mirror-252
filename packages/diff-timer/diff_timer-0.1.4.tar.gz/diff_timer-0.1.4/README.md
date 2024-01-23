# diff_timer

This package includes several timers base on Python.

**Timer:** base on list

**HeapTimer:** base on heap

**WheelTimer:** base on Timing Wheel

## Explanation

**controller:** The Object which is used to create different timers

**tick:** The time interval which is determined by you

**tps:** tick per second

## Installation

```
pip install diff_timer
pip install --upgrade diff_timer
```

## How to use

#### 1、Instantiation

```python
from diff_timer import Controller
INTERVAL = 5
tps = 50
controller = Controller()
controller.initTimer("WHEEL", INTERVAL, tps)
```

#### 2、We need a time driver

```python
TIME_GAP = 1 / tps  # 1 / 50 = 0.02
curTick = 0
while True:
    time.sleep(TIME_GAP)
    controller.tick(curTick)
    curTick += 1
```

#### 3、set timer at any place that you want

```python
from diff_timer import setTimeOut
def test():
    print("this is a test func")

setTimeOut(test, 10, "test_func")
```

**example: test.py**
