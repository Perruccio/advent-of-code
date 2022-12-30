from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import search as aoc_search
from advent_of_code.lib import aoc
import copy


def get_input(file):
    return aoc_parse.map_by_line(aoc.read_input(2022, 12, file), list)


def find_start_end(grid, start_char, end_char):
    start, end = None, None
    for r, row in enumerate(grid):
        if start_char in row:
            start = (r, row.index(start_char))
        if end_char in row:
            end = (r, row.index(end_char))
    return start, end


@aoc.pretty_solution(1)
def part1(grid):
    grid = copy.deepcopy(grid)
    start, end = find_start_end(grid, "S", "E")
    grid[start[0]][start[1]] = "a"
    grid[end[0]][end[1]] = "z"

    def is_end(_, pos):
        return pos == end

    def is_valid(grid, neighbour, pos):
        return ord(grid[neighbour[0]][neighbour[1]]) - ord(grid[pos[0]][pos[1]]) <= 1

    return len(aoc_search.bfs_grid(grid, start, is_end, is_valid)) - 1


@aoc.pretty_solution(2)
def part2(grid):
    start, end = find_start_end(grid, "E", "S")
    grid[start[0]][start[1]] = "z"
    grid[end[0]][end[1]] = "a"
    # bfs
    def is_end(grid, pos):
        return grid[pos[0]][pos[1]] == "a"

    def is_valid(grid, neighbour, pos):
        return ord(grid[pos[0]][pos[1]]) - ord(grid[neighbour[0]][neighbour[1]]) <= 1

    return len(aoc_search.bfs_grid(grid, start, is_end, is_valid)) - 1


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 31
    assert part2(example) == 29

    data = get_input("input.txt")
    assert part1(data) == 504
    assert part2(data) == 500

    print("Test OK")


if __name__ == "__main__":
    test()
