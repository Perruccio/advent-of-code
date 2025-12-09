from math import sqrt, log10
from collections.abc import Iterable


def mean(data):
    return sum(data) / len(data)


def sign(x):
    match x:
        case int() | float():
            return 1 if x > 0 else -1 if x < 0 else 0
        case complex():
            return complex(sign(x.real), sign(x.imag))
        case Iterable():
            return type(x)(*(sign(c) for c in x))
        case _:
            ValueError(f"Cannot compute sign of {type(x)}")


def norm(vector, measure="l2"):
    match measure.lower():
        case "l2":
            return sqrt(sum(c * c for c in vector))
        case "inf":
            return sum(abs(c) for c in vector)
        case _:
            ValueError(f"Unknown measure {measure}")


def complex_modulo(x, mod, shift=0):
    return complex(
        shift.real + (x.real - shift.real) % mod.real, shift.imag + (x.imag - shift.imag) % mod.imag
    )


def hex2bin(hex_digits, fill=True):
    return "".join([bin(int(hex_digit, 16))[2:].zfill(4 * int(fill)) for hex_digit in hex_digits])


def newton(f, fprime, x, y_toll=1e-12, max_iter=1000):
    iter = 0
    while abs(y := f(x)) > y_toll and iter < max_iter:
        # add 1e-16 for safety
        x = x - y / (1e-16 + fprime(x))
        iter += 1
    return x


def secant(f, x1, x2, y_toll=1e-12, max_iter=1000):
    iter = 0
    while abs(y2 := f(x2)) > y_toll and iter < max_iter:
        # add 1e-16 for safety
        x1, x2 = x2, x2 - (x2 - x1) / (1e-16 + y2 - f(x1)) * y2
        iter += 1
    return x2


def n_digits(n, m = 1):
    """Compute the number of digits of n * m"""
    if m != 1:
        assert n > 0
        return int(log10(n) + log10(m)) + 1
    if n == 0: return 1
    if n < 0: return 1 + n_digits(-n)
    return int(log10(n)) + 1


def argmax(iterable, start=0, end=None):
    """Return the (index, value) of the maximum element in the iterable"""
    v = list(iterable)
    if end is None:
        end = len(v)
    mx = max(v[start:end])
    i = v.index(mx, start, end)
    return i, mx

def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]