from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2024, 20, file)
    grid = aoc.parse.as_lines(raw)
    m = {r+1j*c:x for r, line in enumerate(grid) for c, x in enumerate(line)}
    return m


def bfs(m, start):
    # find distance from 'start' to any point (called with 'end')
    res = {start:0}
    q = deque([(0, t:=0, start)])
    seen = {start}
    while q:
        l, _, p = q.popleft()
        res[p] = l
        # visit neighbours
        for step in (1, -1, 1j, -1j):
            new = p + step
            if m[new] != "#" and new not in seen:
                q.append((l+1, t:=t+1, new))
                seen.add(new)
    return res

def dfs(m, start, end):
    # compute path from start to end
    q = [(0, start, [start])]
    seen = {start}
    while q:
        l, p, path = q.pop()
        if p == end:
            return path
        # visit neighbours
        for step in (1, -1, 1j, -1j):
            new = p + step
            if m[new] != "#" and new not in seen:
                q.append((l+1, new, path + [new]))
                seen.add(new)
    return []


def count_cheats(end_dist, cheat_length, path, saving=100):
    res = 0
    for p in path:
        # use cheat: manhattan distance <= cheat_length
        for dr in range(-cheat_length, cheat_length+1):
            # check only points with at manhattand distance at most cheat_length (included)
            for dc in range(-(cheat_length-abs(dr)), cheat_length-abs(dr)+1):
                l_cheat = abs(dr) + abs(dc)
                p2 = p + dr + 1j*dc
                # count if we save at least 'saving'
                if p2 in end_dist and end_dist[p] - end_dist[p2] - l_cheat >= saving:
                    res += 1
    return res


@aoc.pretty_solution(1)
def part1(m):
    start, end = map(lambda x: next(p for p in m if m[p] == x), ["S", "E"])
    path = dfs(m, start, end)
    end_dist = bfs(m, end)
    return count_cheats(end_dist, 2, path)


@aoc.pretty_solution(2)
def part2(m):
    start, end = map(lambda x: next(p for p in m if m[p] == x), ["S", "E"])
    path = dfs(m, start, end)
    end_dist = bfs(m, end)
    return count_cheats(end_dist, 20, path)


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 1369
    assert part2(data) == 979012
    print("Test OK")


if __name__ == "__main__":
    test()
