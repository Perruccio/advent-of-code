from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 12, file)
    grid = aoc_parse.map_by_line(raw, list)
    m = {i + 1j*j: x for i, line in enumerate(grid) for j, x in enumerate(line)}
    return m


def perimeter(region):
    # find perimeter: count the number of outside neighbours from horizontal/vertical sides
    res = 0
    for p in region:
        res += sum(p+step not in region for step in (1, -1, 1j, -1j))
    return res


def n_sides(region):
    # find n of sides = n of angles
    # we must count angle towards inside and outside. a point can form many angles (from 0 to 4)
    # for each point, look at his 4 oblique neighbours:
    # it's a region angle if:
    # - the oblique is not in the region and the 2 adjacent sides are either
    #   both in the region or neither in the region
    # - the oblique is in the region and the 2 adjacent sides are both not 
    res = 0
    for p in region:
        for dr, dc in cart_prod((1, -1), (1j, -1j)):
            l, r, o = p + dr, p + dc, p + dr + dc
            if (l in region) != (r in region):
                continue
            res += (l not in region) or (o not in region)
    return res


def solve(m, part2=False):
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
        # add whole regiont to seen points
        seen |= region
        res += len(region) * (n_sides(region) if part2 else perimeter(region)) 
    return res


@aoc.pretty_solution(1)
def part1(m):
    return solve(m)

@aoc.pretty_solution(2)
def part2(m):
    return solve(m, part2=True)


def test():
    data = get_input("input.txt")
    assert part1(data) == 1400386
    assert part2(data) == 851994
    print("Test OK")


if __name__ == "__main__":
    test()
