from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
import re
from math import prod


def get_input(file):
    raw = aoc.read_input(2023, 2, file)
    return aoc_parse.as_lines(raw)


def find_max_color(game):
    max_color = {}
    # dynamically compute colors used in the game
    all_colors = set(re.findall(fr"{aoc_parse.RE['int']} (\w+)", game))
    for color in all_colors:
        max_color[color] = max(map(int, re.findall("(" + aoc_parse.RE["int"] + ") " + color, game)))
    return max_color


@aoc.pretty_solution(1)
def part1(lines, max_rgb={"red":12, "green":13, "blue":14}):
    res = 0
    for game_id, line in enumerate(lines, 1):
        color_in_game = find_max_color(line)
        # check if possible
        if all(color_in_game[color] <= max_rgb[color] for color in max_rgb):
            res += game_id
    return res


@aoc.pretty_solution(2)
def part2(lines):
    return sum(prod(find_max_color(line).values()) for line in lines)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 2685
    assert part2(data) == 83707
    print("Test OK")


if __name__ == "__main__":
    main()
