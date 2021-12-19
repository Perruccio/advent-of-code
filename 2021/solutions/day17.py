import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
import re
from math import sqrt

def move(x, y, vx, vy, n):
    xn = x + vx * (vx + 1) // 2 - (vx - n) * (vx - n + 1) * (n < vx)
    yn = y + vy * n - n * (n - 1) // 2
    vxn = max(vx - n, 0)
    vyn = vy - n
    return (xn, yn), (vxn, vyn)

def y_max(vy_0):
    return vy_0 * (vy_0 + 1) // 2

def part1(x_min, x_max, y_min, y_max):
    # assume y_min, y_max are non-positive
    if y_min > 0 or y_max > 0:
        raise ValueError("y_min and y_max must be negative")
    for y in range(-y_min, 0, -1):
        n = 2 * y - 1
        # check if it exists vx such that
        # x(t) is in target
        for vx in range(x_min):
            x, _ = move(0, 0, vx, 0, n)[0]
            if x_min <= x <= x_max:
                return y * (y - 1) // 2
    raise ValueError("couldn't find any solution")

def part2(x_min, x_max, y_min, y_max):
    pass

def main(pretty_print = True):
    
    data = input_as_string(prj_path + '/input/day17.txt')

    x_min, x_max, y_min, y_max = map(int, re.findall(RE['int'], data))

    if (pretty_print):
        print_results(1, part1, x_min, x_max, y_min, y_max)
        print_results(2, part2, x_min, x_max, y_min, y_max)
    else:
        return part1(x_min, x_max, y_min, y_max), part2(x_min, x_max, y_min, y_max)
   
if __name__ == "__main__":
    main()