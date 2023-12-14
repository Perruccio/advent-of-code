from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 11, file)
    return aoc_parse.map_by_line(raw, func=str)


def solve(grid, expansion):
    # first find which rows and cols should be expanded
    expand_rows = set(r for r, row in enumerate(grid) if "#" not in row)
    expand_cols = set(c for c, col in enumerate(zip(*grid)) if "#" not in col)
    # compute set of all galaxies
    galaxies = list((r, c) for r, row in enumerate(grid) for c, p in enumerate(row) if p == "#")
    res = 0
    # compute distances
    # NB by construction we always have r1 <= r2. we can avoid computing abs(r2 - r1), min/max(r1, r2)
    for i, (r1, c1) in enumerate(galaxies):
        for r2, c2 in galaxies[i+1:]:
            res += (r2 - r1) + abs(c2 - c1)
            res += (expansion - 1) * sum(r1 < expand_r < r2 for expand_r in expand_rows)
            res += (expansion - 1) * sum(min(c1, c2) < expand_c < max(c1, c2) for expand_c in expand_cols)
    return res


@aoc.pretty_solution(1)
def part1(grid):
    return solve(grid, 2)


@aoc.pretty_solution(2)
def part2(grid):
    return solve(grid, 1000000)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 9445168
    assert part2(data) == 742305960572
    print("Test OK")


if __name__ == "__main__":
    main()
