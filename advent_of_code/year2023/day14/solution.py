from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
import copy


def get_input(file):
    raw = aoc.read_input(2023, 14, file)
    return aoc_parse.as_lines(raw)


def est_load(grid):
    return sum(c + 1 for row in grid for c, p in enumerate(row) if p == "O")


def rotate_clockwise(grid):
    return list(map(lambda s: "".join(s), zip(*grid[::-1])))


def move_east(old_grid):
    grid = copy.deepcopy(old_grid)
    for r, row in enumerate(grid):
        new_row = list(row)
        c = 0
        rocks = 0
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                rocks += 1
                new_row[c] = "."
            elif grid[r][c] == "#":
                new_row[c - rocks : c] = ["O"] * rocks
                rocks = 0
            c += 1
        if rocks:
            new_row[-rocks:] = ["O"] * rocks
        grid[r] = new_row
    return grid


@aoc.pretty_solution(1)
def part1(grid):
    grid = rotate_clockwise(grid)
    grid = move_east(grid)
    return est_load(grid)


@aoc.pretty_solution(2)
def part2(grid):
    grid = rotate_clockwise(grid)
    seen_list = [grid]
    seen = {"".join(grid): 0}
    n = 1000000000
    for i in range(1, n + 1):
        # do 1 complete cycle
        for _ in range(4):
            grid = move_east(grid)
            grid = rotate_clockwise(grid)
        state = "".join(grid)
        if state in seen:
            first_i = seen[state]
            grid = seen_list[first_i + (n - i) % (i - first_i)]
            return est_load(grid)
        seen[state] = i
        seen_list.append(grid)
    return None


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 109466
    assert part2(data) == 94585
    print("Test OK")


if __name__ == "__main__":
    test()
