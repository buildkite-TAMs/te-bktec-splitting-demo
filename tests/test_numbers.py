import time
from src.mathops import is_even


def test_even_true():
    time.sleep(0.7)
    assert is_even(10) is True


def test_even_false():
    time.sleep(0.5)
    assert is_even(7) is False


def test_even_zero():
    time.sleep(0.3)
    assert is_even(0) is True


def test_even_large():
    time.sleep(0.9)
    assert is_even(1_000_000) is True
