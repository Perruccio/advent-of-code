from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import math as aoc_math
from advent_of_code.lib import aoc
from math import sqrt


def get_input(file):
    lines = aoc_parse.as_lines(aoc.read_input(2022, 22, file))
    # store points in a dictionary {point : bool(free)}
    # points are complex numbers, true if free and false if there's a wall
    grid = {}
    for r, line in enumerate(lines[:-2]):
        for c, point in enumerate(line):
            if point == " ":
                continue
            grid[complex(c, r)] = point == "."
    path = lines[-1].replace("R", " R ").replace("L", " L ")
    path = list(map(lambda c: int(c) if c.isnumeric() else c, path.split()))
    return grid, path


def compute_limits(grid):
    # compute col/row limits and their length for modulo operations
    col_limits = {
        r: (
            lo := min(point.real for point in grid if point.imag == r),
            hi := max(point.real for point in grid if point.imag == r),
            hi - lo + 1,
        )
        for r in set(p.imag for p in grid)
    }
    row_limits = {
        c: (
            lo := min(point.imag for point in grid if point.real == c),
            hi := max(point.imag for point in grid if point.real == c),
            hi - lo + 1,
        )
        for c in set(p.real for p in grid)
    }
    return col_limits, row_limits


def wrap_flat(pos, step, n, grid, col_limits, row_limits):
    mod = complex(col_limits[pos.imag][2], row_limits[pos.real][2])
    shift = complex(col_limits[pos.imag][0], row_limits[pos.real][0])
    for _ in range(n):
        new_pos = aoc_math.complex_modulo(pos + step, mod, shift)
        if not grid[new_pos]:
            break
        pos = new_pos
    return pos


def wrap_cube(pos, step, n, grid, side):
    # row, column
    r, c = pos.imag, pos.real
    # delta row, delta column
    dr, dc = step.imag, step.real
    for _ in range(n):
        # new column, new row
        nr, nc = r + dr, c + dc
        # new delta row, new delta column
        ndr, ndc = dr, dc

        # remap all sides, supporting only a specific configuration
        if nr < 0 and side <= nc < 2 * side and dr == -1:
            ndr, ndc = 0, 1
            nr, nc = nc + 2 * side, 0
        elif nc < 0 and 3 * side <= nr < 4 * side and dc == -1:
            ndr, ndc = 1, 0
            nr, nc = 0, nr - 2 * side
        elif nr < 0 and 2 * side <= nc < 3 * side and dr == -1:
            nr, nc = 4 * side - 1, nc - 2 * side
        elif nr >= 4 * side and 0 <= nc < side and dr == 1:
            nr, nc = 0, nc + 2 * side
        elif nc >= 3 * side and 0 <= nr < side and dc == 1:
            ndc = -1
            nr, nc = 3 * side - 1 - nr, 2 * side - 1
        elif nc == 2 * side and 2 * side <= nr < 3 * side and dc == 1:
            ndc = -1
            nr, nc = 3 * side - 1 - nr, 3 * side - 1
        elif nr == side and 2 * side <= nc < 3 * side and dr == 1:
            ndr, ndc = 0, -1
            nr, nc = nc - side, 2 * side - 1
        elif nc == 2 * side and side <= nr < 2 * side and dc == 1:
            ndr, ndc = -1, 0
            nr, nc = side - 1, nr + side
        elif nr == 3 * side and side <= nc < 2 * side and dr == 1:
            ndr, ndc = 0, -1
            nr, nc = nc + 2 * side, side - 1
        elif nc == side and 3 * side <= nr < 4 * side and dc == 1:
            ndr, ndc = -1, 0
            nr, nc = 3 * side - 1, nr - 2 * side
        elif nr == 2 * side - 1 and 0 <= nc < side and dr == -1:
            ndr, ndc = 0, 1
            nr, nc = nc + side, side
        elif nc == side - 1 and side <= nr < 2 * side and dc == -1:
            ndr, ndc = 1, 0
            nr, nc = 2 * side, nr - side
        elif nc == side - 1 and 0 <= nr < side and dc == -1:
            ndc = 1
            nr, nc = 3 * side - 1 - nr, 0
        elif nc < 0 and 2 * side <= nr < 3 * side and dc == -1:
            ndc = 1
            nr, nc = 3 * side - 1 - nr, side

        if not grid[complex(nc, nr)]:
            break

        # update
        r, c = nr, nc
        dr, dc = ndr, ndc
    return complex(c, r), complex(dc, dr)


def password(pos, dir):
    return int(1000 * (1 + pos.imag) + 4 * (1 + pos.real) + {1: 0, 1j: 1, -1: 2, -1j: 3}[dir])


@aoc.pretty_solution(1)
def part1(data):
    # get info
    grid, path = data
    col_limits, row_limits = compute_limits(grid)
    # start at upper-left point, right direction
    pos, dir = complex(col_limits[0][0], 0), 1
    for move in path:
        match move:
            case "L":
                dir /= 1j
            case "R":
                dir *= 1j
            case _:
                pos = wrap_flat(pos, dir, move, grid, col_limits, row_limits)
    return password(pos, dir)


@aoc.pretty_solution(2)
def part2(data):
    # get info
    grid, path = data
    side = int(sqrt(len(grid) // 6))
    # start at upper-left point, right direction
    pos, dir = complex(side, 0), 1
    for move in path:
        match move:
            case "L":
                dir /= 1j
            case "R":
                dir *= 1j
            case _:
                pos, dir = wrap_cube(pos, dir, move, grid, side)
    return password(pos, dir)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 6032
    # example has a different configuration of flattening a cube
    # which is not implemented

    data = get_input("input.txt")
    assert part1(data) == 97356
    assert part2(data) == 120175

    print("Test OK")


if __name__ == "__main__":
    test()
