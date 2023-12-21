from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 16, file)
    return aoc_parse.as_lines(raw)


def simulate(grid, start):
    # do a complete simulation, given starting position and direction
    seen = set()
    # a node is (r, c, dir r, dir c)
    # i.e. position + direction
    q = [start]
    while q:
        # visit new node
        r, c, dr, dc = q.pop()

        # check that node is inside the grid
        if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
            continue
        # check if we've already been here with same direction
        if (r, c, dr, dc) in seen:
            continue

        # flag as visited
        seen.add((r, c, dr, dc))

        # handle bifurcations
        if grid[r][c] == "|" and dc != 0:
            q.append((r - 1, c, -1, 0))
            q.append((r + 1, c, +1, 0))
            continue
        elif grid[r][c] == "-" and dr != 0:
            q.append((r, c - 1, 0, -1))
            q.append((r, c + 1, 0, +1))
            continue

        # steer if necessary
        if grid[r][c] == "\\":
            dr, dc = dc, dr
        if grid[r][c] == "/":
            dr, dc = -dc, -dr

        # move
        q.append((r + dr, c + dc, dr, dc))
    # just discard the directions to compute set of all
    # energized points
    return len({(r, c) for r, c, _, _ in seen})


@aoc.pretty_solution(1)
def part1(grid):
    return simulate(grid, (0, 0, 0, 1))


@aoc.pretty_solution(2)
def part2(grid):
    # just brute force all the simulations independetly
    # we could optimize by keeping track of which cells are energize by which rays
    res = 0
    rows, cols = len(grid), len(grid[0])
    # top and bottom row
    for c in range(cols):
        res = max(res, simulate(grid, (0, c, 1, 0)))
        res = max(res, simulate(grid, (rows - 1, c, -1, 0)))
    # first and last column
    for r in range(rows):
        res = max(res, simulate(grid, (r, 0, 0, 1)))
        res = max(res, simulate(grid, (r, cols-1, 0, -1)))
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 8249
    assert part2(data) == 8444
    print("Test OK")


if __name__ == "__main__":
    main()
