import time
from src.mathops import add, multiply

# Each test sleeps a little to simulate real work, so bktec has meaningful
# *timing* differences to balance across parallel agents (not just test counts).


def test_add_positive():
    time.sleep(0.3)
    assert add(2, 3) == 5


def test_add_negative():
    time.sleep(0.5)
    assert add(-4, 10) == 6


def test_multiply():
    time.sleep(0.8)
    assert multiply(6, 7) == 42


def test_multiply_by_zero():
    time.sleep(0.2)
    assert multiply(99, 0) == 0
