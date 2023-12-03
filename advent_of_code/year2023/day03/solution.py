from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc, geometry


def get_input(file):
    raw = aoc.read_input(2023, 3, file)
    return aoc_parse.map_by_line(raw, func=list)


def touch_symbol(grid, r, c):
    # check if grid[r][c] touches a symbol
    m, n = len(grid), len(grid[0])
    for i, j in geometry.get_neighbours((r, c), (m, n), exclude_diag=False):
        if (not grid[i][j].isdigit()) and grid[i][j] != ".":
            return True
    return False


def get_number(grid, r, c):
    # start from position inside a number in the grid
    # and expand left and right to reconstruct the whole number
    if not (0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c].isdigit()):
        return None
    # go left until first digit
    res = [grid[r][c]]
    begin = c
    while 0 <= c-1 and grid[r][c-1].isdigit():
        res.append(grid[r][c-1])
        c -= 1
    res = res[::-1]
    # go right until finished
    c = begin
    while c+1 < len(grid[r]) and grid[r][c+1].isdigit():
        res.append(grid[r][c+1])
        c += 1
    return int(''.join(res))


@aoc.pretty_solution(1)
def part1(grid):
    res = 0
    # loop through the grid
    # when number is encountered, 
    # reconstruct whole number and check if it touches any symbol
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            part = []
            touches_symbol = False
            while c < len(row) and row[c].isdigit():
                part.append(row[c])
                touches_symbol |= touch_symbol(grid, r, c)
                c += 1
            c += 1
            res += int(''.join(part)) if touches_symbol else 0
    return res
            

@aoc.pretty_solution(2)
def part2(grid):
    res = 0
    # scan grid and look for '*'.
    # when one is encountered, compute all adjacent parts
    # and check if only two parts are touched.
    # NB beware of particular vertical case
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != "*":
                continue
            parts = []
            # left and right
            for dc in (-1, 1):
                if part := get_number(grid, r, c + dc):
                    parts.append(part)
            # up and down. NB if up is empty, may touch 2 numbes (up-left and up-right)
            # same for down
            for dr in (-1, 1):
                if vertical := get_number(grid, r + dr, c):
                    parts.append(vertical)
                else:
                    # diagonals
                    for dc in (-1, 1):
                        if diag := get_number(grid, r+dr, c+dc):
                            parts.append(diag)
            if len(parts) == 2:
                res += parts[0] * parts[1]
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 559667
    assert part2(data) == 86841457
    print("Test OK")


if __name__ == "__main__":
    main()
