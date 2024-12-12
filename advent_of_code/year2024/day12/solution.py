from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 12, file)
    grid = aoc_parse.map_by_line(raw, list)
    m = {i + 1j*j: x for i, line in enumerate(grid) for j, x in enumerate(line)}
    return m


@aoc.pretty_solution(1)
def part1(m):
    seen = set()
    res = 0
    for start in m:
        if start in seen: continue
        # find region with DFS
        region = set()
        q = [start]
        while q:
            p = q.pop()
            region.add(p)
            for step in (1, -1, 1j, -1j):
                p2 = p + step
                if p2 not in m or m[p2] != m[p] or p2 in region:
                    continue
                q.append(p2)
        seen |= region
        # find perimeter: count the number of outside neighbours
        perimeter = 0
        for p in region:
            perimeter += sum(p+step not in region for step in (1, -1, 1j, -1j))
        res += len(region) * perimeter
    return res


@aoc.pretty_solution(2)
def part2(data):
    ...

def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 1400386
    # assert part2(data) == 
    print("Test OK")


if __name__ == "__main__":
    main()
