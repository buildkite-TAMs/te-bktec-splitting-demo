import time
from src.mathops import reverse


def test_reverse_word():
    time.sleep(0.6)
    assert reverse("buildkite") == "etikdliub"


def test_reverse_palindrome():
    time.sleep(0.4)
    assert reverse("level") == "level"


def test_reverse_empty():
    time.sleep(0.2)
    assert reverse("") == ""


def test_reverse_twice():
    time.sleep(1.0)
    assert reverse(reverse("kite")) == "kite"
