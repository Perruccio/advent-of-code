from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 16, file)
    m = {r + 1j*c:x for r, line in enumerate(aoc_parse.as_lines(raw))
                    for c, x in enumerate(line) if x != "#"}
    return m


def solve(m, part2=False):
    start, end = map(lambda c: next(p for p, x in m.items() if x == c), ("S", "E"))
    # keep track of best score
    best = 1e9
    # best score so far at given position with given direction
    seen = defaultdict(lambda:best)
    # all points in optimal paths
    res2 = set()
    # t is just a tie breaker for heapq because complex
    # numbers are not comparable
    q = [(0, t:=0, start, 1j, [start])]
    # Dijkstra
    while q:
        score, _, p, v, path = heappop(q)
        if score > seen[p, v]:
            continue
        seen[p, v] = score
        if p == end:
            if not part2:
                return score
            best = score
            res2 |= set(path)
            continue
        # move forward or rotate and take a step (avoid useless rotations)
        for rot, points in (1, 1), (1j, 1001), (-1j, 1001):
            new = p + v*rot
            if new in m:
                heappush(q, (score + points, t:=t+1, new, v*rot, path + [new] if part2 else None))
    return len(res2)


@aoc.pretty_solution(1)
def part1(m):
    return solve(m)


@aoc.pretty_solution(2)
def part2(m):
    return solve(m, part2=True)

def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 107512
    assert part2(data) == 561
    print("Test OK")


if __name__ == "__main__":
    test()
