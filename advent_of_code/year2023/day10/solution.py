from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 10, file)
    return aoc_parse.as_lines(raw)


def move(grid, curr, last):
    r, c = curr
    match grid[r][c]:
        case "|":
            r, c = (r+1, c) if last == (r-1, c) else (r-1, c)
        case "-":
            r, c = (r, c+1) if last == (r, c-1) else (r, c-1)
        case "F":
            r, c = (r, c+1) if last == (r+1, c) else (r+1, c)
        case "7":
            r, c = (r+1, c) if last == (r, c-1) else (r, c-1)
        case "J":
            r, c = (r, c-1) if last == (r-1, c) else (r-1, c)
        case "L":
            r, c = (r, c+1) if last == (r-1, c) else (r-1, c)
    # return new position (r, c) and new last position (curr)
    return (r, c), curr


def get_pipes(grid):
    rows, cols = len(grid), len(grid[0])
    # find start
    r = int(list(filter(lambda r: grid[r].find("S") >= 0, range(rows)))[0])
    c = grid[r].find("S")
    # manually do first step
    last = r, c
    if r + 1 < rows and grid[r+1][c] in "|JL":
        r, c = r+1, c
    elif r - 1 >= 0 and grid[r-1][c] in "|7F":
        r, c = r-1, c
    elif c+1 < cols and grid[r][c+1] in "-7J":
        r, c = r, c+1
    else:
        r, c = r, c-1
    # move inside the pipes
    pipes = set([(r, c)])
    while True:
        (r, c), last = move(grid, (r, c), last)
        pipes.add((r, c))
        if grid[r][c] == "S":
            break
    return pipes


@aoc.pretty_solution(1)
def part1(grid):
    pipes = get_pipes(grid)
    return len(pipes) // 2


@aoc.pretty_solution(2)
def part2(grid):
    pipes = get_pipes(grid)
    rows, cols = len(grid), len(grid[0])
    res = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) in pipes:
                continue
            # (r, c) is inside iff you cross the borders an odd
            # number of times in every direction
            # just take the right direction for simplicity
            # NB we also need to count angles like FJ and L7, but not LJ or F7
            # e.g. |F7L7 --> 2 walls because we count | and L7
            # NB angles always come in pair, but pair of angles in same direction must not be counted
            # this is why we take the min
            vertical_pipes = sum(grid[r][c2] == "|" and (r, c2) in pipes for c2 in range(c+1, cols))
            up_angle = sum(grid[r][c2] in "JL" and (r, c2) in pipes for c2 in range(c+1, cols))
            down_angle = sum(grid[r][c2] in "7F" and (r, c2) in pipes for c2 in range(c+1, cols))
            res += (vertical_pipes + min(up_angle, down_angle)) % 2
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 6875
    assert part2(data) == 471
    print("Test OK")


if __name__ == "__main__":
    main()
