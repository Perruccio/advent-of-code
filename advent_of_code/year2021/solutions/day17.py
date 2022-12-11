import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse
import re

"""
given (x0, y0) initial position and (vx0, vy0) initial velocity,
knowint the acceleration and friction,
the equations of the motion are (position updated before velocity):

---
| x(n) = x0 + vx0 * (vx0 + 1) / 2 - (vx0 - n) * (vx0 - n + ) / 2 * (n < vx0)
| y(n) = y0 + vy0 * n - n * (n - 1) / 2
|
| vx(n) = max(vx0 - n, 0)
| vy(n) = vy0 - n
---

in our case x(0) = y(0) = 0

if vy0 > 0, max height is hit when vy(n_hi) = 0
i.e. when n_hi = vy0, and y(n_hi) = vy0 * (vy0 + 1) / 2

"""

def move(x, y, vx, vy, n):
    xn = x + vx * (vx + 1) // 2 - (vx - n) * (vx - n + 1) // 2 * (n < vx)
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
    # we could find the solution without brute force
    # computing x(n), y(n) everytime from (0,0) is useless
    # but i wanted to test the dynamics
    res = 0
    for vx in range(1, x_max + 1):
        for vy in range(y_min, -y_min + 1):
            n, xn, yn = 0, 0, 0
            while xn <= x_max and yn >= y_min:
                if x_min <= xn <= x_max and y_min <= yn <= y_max:
                    res += 1
                    break
                n += 1
                xn, yn = move(0, 0, vx, vy, n)[0]
    return res


def main(pretty_print = True):

    data = aoc_parse.input_as_string(prj_path + '/year2021/input/day17.txt')

    x_min, x_max, y_min, y_max = map(int, re.findall(aoc_parse.RE['int'], data))

    if (pretty_print):
         aoc_output.output_procedure(1, part1, True, x_min, x_max, y_min, y_max)
         aoc_output.output_procedure(2, part2, True, x_min, x_max, y_min, y_max)
    else:
        return part1(x_min, x_max, y_min, y_max), part2(x_min, x_max, y_min, y_max)

if __name__ == "__main__":
    main()