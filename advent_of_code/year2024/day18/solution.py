from advent_of_code.lib.all import *


def get_input(file):
    points = aoc_parse.map_by_line(aoc.read_input(2024, 18, file), aoc_parse.get_ints)
    rows = cols = 71
    m = {r+1j*c for r in range(rows) for c in range(cols)}
    return m, rows, cols, points


def solve(m, start, end):
    assert start in m and end in m
    # position, length of path
    q = deque([(start, 0)])
    seen = {start}
    # BFS
    while q:
        p, l = q.popleft()
        if p == end:
            return l
        for step in (1, -1, 1j, -1j):
            new = p + step
            if new in m and new not in seen:
                q.append((new, l+1))
                # NB it's important to add states to seen here
                # otherwise we might append the same state more time
                seen.add(new)
    return None


@aoc.pretty_solution(1)
def part1(m, rows, cols, points):
    for r, c in points[:1204]:
        m.remove(r+1j*c)
    return solve(m, 0, (rows-1) + 1j * (cols-1))


@aoc.pretty_solution(2)
def part2(m, rows, cols, points):
    for r, c in points[:2500]:
        m.remove(r+1j*c)

    for r, c in points[2500:]:
        m.remove(r+1j*c)
        res = solve(m, 0, (rows-1) + 1j * (cols-1))
        if res is None:
            return f"{r},{c}"
    return None


def test():
    data = get_input("input.txt")
    assert part1(*deepcopy(data)) == 314
    assert part2(*data) == "15,20"
    print("Test OK")


if __name__ == "__main__":
    test()
