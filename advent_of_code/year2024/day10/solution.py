from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 10, file)
    grid = aoc_parse.map_by_line(raw, lambda line: list(map(int, line)))
    # create grid in a dictionary (for easy boundary checking)
    # using complex numbers 'cause it's cool... easy to move
    m = {i + 1j*j:x for i, line in enumerate(grid) for j, x in enumerate(line)}
    return m


def solve(m, part2):
    starts = [p for p, x in m.items() if x == 0]
    res = 0
    for start in starts:
        peeks = set()
        # DFS
        q = [start]
        while q:
            pos = q.pop()
            # check hiking is over
            if m[pos] == 9:
                # no double counting is possible
                # every time we arrive here it's from a different path
                if part2: res += 1
                else: peeks.add(pos)
                continue
            # explore new positions
            for step in (1, -1, 1j, -1j):
                new_pos = pos + step
                # check new_pos in the map and one step higher
                if new_pos in m and m[pos] + 1 == m[new_pos]:
                    q.append(new_pos)
        if not part2:
            res += len(peeks)
    return res


@aoc.pretty_solution(1)
def part1(data):
    return solve(data, part2=False)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, part2=True)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 489
    assert part2(data) == 1086
    print("Test OK")


if __name__ == "__main__":
    test()
