# py
from typing import List
import time

RE = {"int": r"[+-]?\d+"}


def input_as_string(filename: str) -> str:
    """Returns the content of the input file as a string"""
    with open(filename) as f:
        return f.read().rstrip("\n")


def input_as_lines(filename: str) -> List[str]:
    """Return a list where each line in the input file is an element of the list"""
    return input_as_string(filename).split("\n")


def map_input_lines(filename: str, func) -> List:
    """Returns the content of the input file as a list of mapped lines"""
    return list(map(func, input_as_lines(filename)))


def input_as_list_of_lists(filename: str, delim: str = "", func=int) -> List[List]:
    """Parse input where data are lists separated by a delimiter line"""
    return list(
        map(
            lambda line: [func(x) for x in line.split("\n")],
            input_as_string(filename).split("\n" + delim + "\n"),
        )
    )


def print_result(part, func, *arg, **kw):
    t = time.time_ns()
    ans = func(*arg, **kw)
    ns = time.time_ns() - t  # nanoseconds
    print(f"Part {part}: {ans} \t({time_measure(ns)})")
    return ans


def pretty_solution(part):
    def decorator(func):
        def wrapper(*arg, **kw):
            t = time.time_ns()
            ans = func(*arg, **kw)
            ns = time.time_ns() - t  # nanoseconds
            print(f"Part {part}: {ans} \t({time_measure(ns)})")
            return ans

        return wrapper

    return decorator


def time_measure(ns):
    # compute appropriate time measure units
    i = 0
    while ns >= 1000 and i < 3:
        ns /= 1000
        i += 1
    return str(f"{ns:.2f}") + " " + ["ns", "us", "ms", "s"][i]


def sign(x: float) -> float:
    return 1 if x > 0 else -1 if x < 0 else 0


def mean(l):
    return sum(l) / len(l)


def sorted_string(s):
    s = sorted(s)
    return "".join(s)


def get_neighbours(pos, end, exclude_diag=False):
    """return the position of the neighbours of pos in a 2d matrix"""
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if not exclude_diag:
        shifts += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in shifts:
        i2, j2 = pos[0] + di, pos[1] + dj
        if 0 <= i2 < end[0] and 0 <= j2 < end[1]:
            yield i2, j2


def hex2bin(hex_digits, fill=True):
    return "".join(
        [bin(int(hex_digit, 16))[2:].zfill(4 * int(fill)) for hex_digit in hex_digits]
    )


def print_image(image):
    for line in image:
        for c in line:
            if c:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def intersect1d(aa, bb):
    l = max(aa[0], bb[0])
    r = min(aa[1], bb[1])
    return (l, r) if l <= r else None


class Cuboid:
    def __init__(self, xx, yy, zz):
        assert xx[0] <= xx[1] and yy[0] <= yy[1] and zz[0] <= zz[1]
        self.xx = xx
        self.yy = yy
        self.zz = zz

    def is_small(self, l=50):
        return all(-l <= tt[0] and tt[1] <= l for tt in [self.xx, self.yy, self.zz])

    def volume(self):
        return (
            (self.xx[1] - self.xx[0] + 1)
            * (self.yy[1] - self.yy[0] + 1)
            * (self.zz[1] - self.zz[0] + 1)
        )

    def intersect(self, other):
        xx = intersect1d(self.xx, other.xx)
        yy = intersect1d(self.yy, other.yy)
        zz = intersect1d(self.zz, other.zz)
        if any([t is None for t in [xx, yy, zz]]):
            return None
        return Cuboid(xx, yy, zz)
