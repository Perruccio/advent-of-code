from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2025, 7, file)
    lines = aoc.parse.as_lines(raw)
    rows, cols = len(lines), len(lines[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if lines[r][c] == "S")
    splitters = set((r, c) for r in range(rows) for c in range(cols) if lines[r][c] == "^")
    return rows, start, splitters


@aoc.pretty_solution(1)
def part1(data):
    rows, start, splitters = data
    seen = set()
    res = 0
    q = set([start])
    while q:
        r, c = q.pop()
        # out of scope
        if r >= rows:
            continue
        nxt = (r+1, c)
        # split
        if nxt in splitters:
            q.add((r+1, c-1))
            q.add((r+1, c+1))
            # count if not already counted
            if nxt not in seen:
                res += 1
                seen.add(nxt)
        else:
            q.add(nxt)
    return res


@aoc.pretty_solution(2)
def part2(data):
    rows, start, splitters = data

    @cache
    def dp(r, c):
        """dp(r,c) = solution if starting from (r, c)"""
        if r == rows:
            return 1
        if (r+1, c) in splitters:
            return dp(r+1, c-1) + dp(r+1, c+1)
        else:
            return dp(r+1, c)
    
    return dp(*start)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 1622
    assert part2(data) == 10357305916520
    print("Test OK")


if __name__ == "__main__":
    test()
