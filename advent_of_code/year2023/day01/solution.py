from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 1, file)
    return aoc_parse.as_lines(raw)


@aoc.pretty_solution(1)
def part1(lines):
    # get all ints from line, extract first and last, add directly the last digit and 10*first digit
    return sum(map(lambda digits: 10*digits[0] + digits[-1], map(aoc_parse.get_digits, lines)))


@aoc.pretty_solution(2)
def part2(lines):
    def compute_value(line):
        first, last = None, None
        for i, c in enumerate(line):
            if c.isdigit():
                first, last = first or int(c), int(c)
            for d, w in enumerate(("one", "two", "three", "four", "five", "six", "seven", "eight", "nine"), 1):
                if line[i: i + len(w)] == w:
                    first, last = first or d, d
        return 10*first + last
    return sum(map(compute_value, lines))


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 56465
    assert part2(data) == 55902
    print("Test OK")


if __name__ == "__main__":
    main()
