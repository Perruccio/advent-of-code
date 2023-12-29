from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 23, file)
    return aoc_parse.as_lines(raw)


def solve(data, ice):
    grid = {c + r*1j : tile for r, row in enumerate(data) for c, tile in enumerate(row) if tile != "#"}
    start, end = 1, len(data[0]) - 2 + (len(data) - 1)*1j
    q = [(start, set(), 0)]
    moves = {"<":(-1,), ">":(+1,), "^": (-1j,), "v":(+1j,), ".":(1, -1, 1j, -1j)}
    res = 0
    while q:
        pos, seen, steps = q.pop()
        if pos == end:
            res = max(res, steps)
            continue
        
        for move in moves[grid[pos]] if ice else moves["."]:
            new_pos = pos + move
            if new_pos in seen or new_pos not in grid:
                continue
            q.append((new_pos, seen | {pos}, steps + 1))
    return res


@aoc.pretty_solution(1)
def part1(data):
    return solve(data, True)

@aoc.pretty_solution(2)
def part2(data):
    ...


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 2230
    # assert part2(data) == None
    print("Test OK")


if __name__ == "__main__":
    main()
