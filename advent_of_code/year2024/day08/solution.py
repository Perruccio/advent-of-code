from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 8, file)
    grid = aoc_parse.map_by_line(raw, list)
    
    # using complex numbers cause they're cool
    antennas = defaultdict(list)
    for r, line in enumerate(grid):
        for c, x in enumerate(line):
            if x != ".":
                antennas[x].append(r + 1j*c)
    return len(grid), len(grid[0]), antennas


def in_bound(p, rows, cols):
    return 0 <= p.real < rows and 0 <= p.imag < cols


@aoc.pretty_solution(1)
def part1(rows, cols, antennas):
    res = set()
    for _, points in antennas.items():
        l = len(points)
        # just check every pair of points. we check every pair twice
        # to account for both new points without code repetition
        for i in range(l):
            for j in range(l):
                if i == j: continue
                new = points[j] + (points[j] - points[i])
                if in_bound(new, rows, cols):
                    res.add(new)
    return len(res)


@aoc.pretty_solution(2)
def part2(rows, cols, antennas):
    res = set()
    for _, points in antennas.items():
        l = len(points)
        for i in range(l):
            for j in range(i+1, l):
                step = points[j] - points[i]
                # start from one point, and add line step by step
                # for both directions
                for dir in (-1, 1):
                    pos = points[i]
                    while in_bound(pos, rows, cols):
                        res.add(pos)
                        pos += step*dir
    return len(res)


def main():
    data = get_input("input.txt")
    part1(*data)
    part2(*data)


def test():
    data = get_input("input.txt")
    assert part1(*data) == 289
    assert part2(*data) == 1030
    print("Test OK")


if __name__ == "__main__":
    main()
