# Trivial functions under test. The point of this repo is bktec *test splitting*,
# not the code — so everything here is intentionally obvious.
def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def is_even(n):
    return n % 2 == 0


def reverse(s):
    return s[::-1]
