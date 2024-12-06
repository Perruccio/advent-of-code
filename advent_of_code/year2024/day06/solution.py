from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 6, file)
    return aoc_parse.map_by_line(raw, list)

def rotate(dir):
    return dir[1], -dir[0]

def advance(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]

def simulate(grid, pos, dir):
    seen = defaultdict(set) | {pos:{dir}}
    loop = False
    while 1:
        nxt = advance(pos, dir)
        if nxt not in grid:
            break
        if grid[nxt] == "#":
            dir = rotate(dir)
        else:
            pos = nxt
            if loop := pos in seen and dir in seen[pos]:
                break
            seen[pos].add(dir)
    return seen, loop


@aoc.pretty_solution(1)
def part1(data):
    grid = {(i, j):data[i][j] for i in range(len(data)) for j in range(len(data[0]))}
    start = next(((i, j) for i, j in grid if grid[i, j] == "^"))
    seen, _ = simulate(grid, start, (-1, 0))
    return len(seen)

@aoc.pretty_solution(2)
def part2(data):
    grid = {(i, j):data[i][j] for i in range(len(data)) for j in range(len(data[0]))}
    start = next(((i, j) for i, j in grid if grid[i, j] == "^"))
    seen, _ = simulate(grid, start, (-1, 0))
    res = 0
    # brute force: put the rock at every seen position
    for pos in seen:
        if pos == start:
            continue
        grid[pos] = "#"
        _, loop = simulate(grid, start, (-1, 0))
        # backtrack
        grid[pos] = "."
        res += loop
    return res

def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 4826
    assert part2(data) == 1721
    print("Test OK")


if __name__ == "__main__":
    test()
