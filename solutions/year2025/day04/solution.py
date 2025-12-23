from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2025, 4, file)
    lines = aoc.parse.as_lines(raw)
    res = defaultdict(lambda:{})
    for r, line in enumerate(lines):
        for c, point in enumerate(line):
            res[r][c] = point
    return res


def get_neighbors(data, r, c):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dc == 0 and dr == 0:
                continue
            nr, nc = r + dr, c + dc
            if nr in data and nc in data[nr]:
                yield nr, nc, data[nr][nc]


@aoc.pretty_solution(1)
def part1(data):
    res = 0
    for r, line in data.items():
        for c, point in line.items():
            if point == '@':
                neighbor_points = get_neighbors(data, r, c)
                if sum(n == "@" for _, _, n in neighbor_points) < 4:
                    res += 1
    return res


@aoc.pretty_solution(2)
def part2(data):
    res = 0
    # keep a stack of points to explore
    q = set(((r, c) for r in data for c in data[r] if data[r][c] == '@'))

    while q:
        r, c = q.pop()
        neighbor_points = list(get_neighbors(data, r, c))
        # the only way a new point can become valid
        # is when a neighbour is cleaned
        if sum(n == "@" for _, _, n in neighbor_points) < 4:
            res += 1
            data[r][c] = '.'
            q.update(((r, c) for r, c, n in neighbor_points if n == "@"))
        
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 1428
    assert part2(data) == 8936
    print("Test OK")


if __name__ == "__main__":
    test()
