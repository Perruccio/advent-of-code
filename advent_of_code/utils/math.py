def mean(l):
    return sum(l) / len(l)


def sign(x: float) -> float:
    return 1 if x > 0 else -1 if x < 0 else 0


def complex_sign(x: complex) -> complex:
    return complex((x.real > 0) - (x.real < 0), (x.imag > 0) - (x.imag < 0))


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
