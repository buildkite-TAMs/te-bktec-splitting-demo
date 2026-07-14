import time
from src.mathops import add

# Deliberately the slowest file — this is what makes test splitting worthwhile.
# bktec should learn from timing history and keep this off the critical path.


def test_slow_one():
    time.sleep(1.5)
    assert add(1, 1) == 2


def test_slow_two():
    time.sleep(1.5)
    assert add(10, 20) == 30


def test_slow_three():
    time.sleep(2.0)
    assert add(100, 200) == 300
