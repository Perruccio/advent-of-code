import pathlib

import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse


def get_input(file):
    file_path = str(pathlib.Path(__file__).parent) + "/" + file
    return aoc_parse.map_input_lines(file_path, lambda line: [int(x) for x in line])


def get_directions(grid, r, c):
    """Get the 4 iterators starting from (r, c) excluded, with True when other
    trees are lower than grid[r][c]"""
    height = grid[r][c]
    east = (tree < height for tree in grid[r][c + 1:])
    west = (tree < height for tree in reversed(grid[r][:c]))
    south = (grid[i][c] < height for i in range(r + 1, len(grid)))
    north = (grid[i][c] < height for i in range(r - 1, -1, -1))
    return east, west, south, north


@aoc_output.pretty_solution(1)
def part1(grid):
    visible = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            # visible if any of the directions has all trees lower
            visible += any(map(all, get_directions(grid, r, c)))
    return visible


@aoc_output.pretty_solution(2)
def part2(grid):
    max_score = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            score = 1
            # directions as list to use len(). Not efficient but more readable
            for direction in map(list, get_directions(grid, r, c)):
                # compute the first index where the tree is not lower than current
                # if every tree is lower, than every tree (len(direction))
                score *= next(
                    (i + 1 for i, lower in enumerate(direction) if not lower),
                    len(direction),
                )
            max_score = max(max_score, score)
    return max_score


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 21
    assert part2(example) == 8

    data = get_input("input.txt")
    assert part1(data) == 1796
    assert part2(data) == 288120

    print("Test OK")


if __name__ == "__main__":
    main()
