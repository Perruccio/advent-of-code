from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 13, file)
    grids = [[]]
    for line in aoc_parse.as_lines(raw):
        if line == "":
            grids.append([])
            continue
        grids[-1].append(line)
    return grids


def horizontal_reflection(grid, old=None):
    # compute n of rows above reflection
    # ignore reflection at r = old
    for i, row in enumerate(grid[:-1]):
        # check if two consecutive rows are identical
        if row == grid[i+1] and old not in {i, i+1}:
            # check it actually is a reflection
            r1, r2 = i-1, i+2
            while 0 <= r1 and r2 < len(grid):
                if grid[r1] != grid[r2]:
                    break
                r1 -= 1
                r2 += 1
            else:
                return i+1
    return None


@aoc.pretty_solution(1)
def part1(data):
    res = 0
    for grid in data:
        r = horizontal_reflection(grid)
        # just transpose the whole grid
        c = horizontal_reflection(list(zip(*grid)))
        res += 100 * (r or 0) + (c or 0)
    return res


@aoc.pretty_solution(2)
def part2(data):
    res = 0
    for grid in data:
        r = horizontal_reflection(grid)
        c = horizontal_reflection(list(zip(*grid)))
        # try to change one cell at at time
        found = False
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                # change whole row because strings are immutable
                grid[i] = row[:j] + ("#" if cell == "." else ".") + row[j+1:]
                # check if reflection, excluding old ones
                r2 = horizontal_reflection(grid, r)
                c2 = horizontal_reflection(list(zip(*grid)), c)
                if r2 or c2:
                    res += 100 * (r2 or 0) + (c2 or 0)
                    found = True
                    break
                # restore old row
                grid[i] = row
            # early break if already found
            if found:
                break
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 34100
    assert part2(data) == 33106
    print("Test OK")


if __name__ == "__main__":
    main()
