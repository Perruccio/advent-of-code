from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2023, 23, file)
    return aoc.parse.as_lines(raw)


def is_intersection(grid, pos):
    paths = 0
    for move in (1, -1, 1j, -1j):
        if pos + move in grid:
            paths += 1
    return paths >= 3


def solve(data, ice):
    # convert grid to dictionary of complex : tile
    grid = { r + c * 1j: tile for r, row in enumerate(data) for c, tile in enumerate(row) if tile != "#" }
    # find start and end points
    start = next(filter(lambda p: p.real == 0, grid))
    end = next(filter(lambda p: p.real == len(data) - 1, grid))

    # construct the shrunk graph from intersection node to other intersection nodes
    # assuming the map is like a maze
    moves = {"<": (-1j,), ">": (1j,), "^": (-1,), "v": (1,), ".": (1, -1, 1j, -1j)}
    nodes = {start, end} | set(filter(lambda pos: is_intersection(grid, pos), grid))
    graph = defaultdict(defaultdict)
    for node in nodes:
        q = [(node, 0)]
        seen = set()
        while q:
            point, steps = q.pop()
            if point not in grid or point in seen:
                continue
            seen.add(point)
            if point in nodes and point != node:
                graph[node][point] = steps
                continue
            for move in moves[grid[point]] if ice else moves["."]:
                q.append((point + move, steps + 1))

    # do the brute force on the shrunk graph
    q = [(start, set(), 0)]
    res = 0
    while q:
        pos, seen, steps = q.pop()
        if pos == end:
            res = max(res, steps)
            continue

        for nxt, dist in graph[pos].items():
            if nxt in seen:
                continue
            q.append((nxt, seen | {pos}, steps + dist))
    return res


@aoc.pretty_solution(1)
def part1(data):
    return solve(data, True)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, False)


def main():
    data = get_input("example.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 2230
    assert part2(data) == 6542
    print("Test OK")


if __name__ == "__main__":
    test()
