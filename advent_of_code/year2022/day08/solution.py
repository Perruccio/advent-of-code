import pathlib
import advent_of_code.utils.aoc as aoc


def get_input(file):
    file_path = str(pathlib.Path(__file__).parent) + "/" + file
    return aoc.map_input_lines(file_path, lambda line: [int(x) for x in line])


def get_directions(grid, r, c):
    """Get the 4 iterators starting from (r, c) excluded, with True when other tree
    is lower than grid[r][c]"""
    height = grid[r][c]
    east = (tree < height for tree in grid[r][c + 1 :])
    west = (tree < height for tree in reversed(grid[r][:c]))
    south = (grid[i][c] < height for i in range(r + 1, len(grid)))
    north = (grid[i][c] < height for i in range(r - 1, -1, -1))
    return east, west, south, north


@aoc.pretty_solution(1)
def part1(grid):
    visibles = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            # visibile if any of the directions has all trees lower
            visibles += any(map(all, get_directions(grid, r, c)))
    return visibles


@aoc.pretty_solution(2)
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
    input = get_input("input.txt")
    part1(input)
    part2(input)


def test():
    example = get_input("example.txt")
    assert part1(example) == 21
    assert part2(example) == 8

    input = get_input("input.txt")
    assert part1(input) == 1796
    assert part2(input) == 288120

    print("Test OK")


if __name__ == "__main__":
    test()
