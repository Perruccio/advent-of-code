# py
from typing import List
import time

def input_as_string(filename:str) -> str:
    """Returns the content of the input file as a string"""
    with open(filename) as f:
        return f.read().rstrip("\n")

def input_as_lines(filename:str) -> List[str]:
    """Return a list where each line in the input file is an element of the list"""
    return input_as_string(filename).split("\n")
    
def map_input_lines(filename:str, func) -> List:
    """Returns the content of the input file as a list of mapped lines"""
    return list(map(func, input_as_lines(filename)))

def print_results(part, func, *arg, **kw):
    t = time.time_ns()
    ans = func(*arg, **kw)
    ns = time.time_ns() - t #nanoseconds
    print(f"Part {part}: {ans} ({time_measure(ns)})")
    return ans

def time_measure(ns):
    # compute appropriate time measure units
    i = 0
    while ns >= 1000 and i < 3:
        ns /= 1000
        i += 1
    return str(f'{ns:.2f}') + " " + ["ns", "us", "ms", "s"][i]

def sign(x:float) -> float:
    return 1 if x > 0 else -1 if x < 0 else 0

def mean(l):
    return sum(l) / len(l)
    
def sorted_string(s):
    s = sorted(s)
    return ''.join(s)

def get_neighbours(pos, end, exclude_diag=False):
    """ return the position of the neighbours of pos in a 2d matrix"""
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if not exclude_diag:
        shifts += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in shifts:
        i2, j2 = pos[0] + di, pos[1] + dj
        if 0 <= i2 < end[0] and 0 <= j2 < end[1]:
            yield i2, j2

def hex2bin(hex_digits, fill=True):
    return "".join([bin(int(hex_digit, 16))[2:].zfill(4 * int(fill)) for hex_digit in hex_digits])