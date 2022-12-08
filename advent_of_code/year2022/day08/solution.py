import pathlib
import advent_of_code.utils.aoc as aoc


def get_input(file):
    file_path = str(pathlib.Path(__file__).parent) + "/" + file
    return aoc.map_input_lines(file_path, lambda line: [int(x) for x in line])


def is_visibile_from(grid, point, direction):
    """Given a direction in the form (dx, dy) unitary, check if point is visibile
    and also return n of trees visibile from point"""
    (x, y), (dx, dy) = point, direction
    h = grid[x][y]
    trees_seen = 0
    # make first step to avoid cumbersome checks
    x, y = x + dx, y + dy
    # while still in the grid
    while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        trees_seen += 1
        if grid[x][y] >= h:
            return False, trees_seen
        x, y = x + dx, y + dy
    return True, trees_seen


def is_visible(grid, point):
    """Check if point is visible from any direction and compute also its scenic score"""
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    scenic_score, visible = 1, False
    for direction in directions:
        visible_from, score = is_visibile_from(grid, point, direction)
        visible |= visible_from
        scenic_score *= score
    return visible, scenic_score


@aoc.pretty_solution(1)
def part1(input):
    # compute all visibile spots
    return sum(
        [
            sum([is_visible(input, (x, y))[0] for x in range(len(input))])
            for y in range(len(input[0]))
        ]
    )


@aoc.pretty_solution(2)
def part2(input):
    # compute max possible scenic score
    return max(
        [
            max([is_visible(input, (x, y))[1] for x in range(len(input))])
            for y in range(len(input[0]))
        ]
    )


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
