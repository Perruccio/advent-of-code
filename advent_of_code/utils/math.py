def mean(l):
    return sum(l) / len(l)


def sign(x: float) -> float:
    return 1 if x > 0 else -1 if x < 0 else 0


def complex_sign(x: complex) -> complex:
    return complex((x.real > 0) - (x.real < 0), (x.imag > 0) - (x.imag < 0))


def hex2bin(hex_digits, fill=True):
    return "".join([bin(int(hex_digit, 16))[2:].zfill(4 * int(fill)) for hex_digit in hex_digits])
