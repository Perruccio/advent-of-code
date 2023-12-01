from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 1, file)
    return aoc_parse.as_lines(raw)


@aoc.pretty_solution(1)
def part1(lines):
    # get all ints from line, extract first and last, add directly the last digit and 10*first digit
    return sum(map(lambda ints: 10 * int(str(ints[0])[0]) + ints[-1]%10, map(aoc_parse.get_ints, lines)))


@aoc.pretty_solution(2)
def part2(lines):
    def compute_value(line):
        digits = {
            "one":1,
            "two":2,
            "three":3,
            "four":4,
            "five":5,
            "six":6,
            "seven":7,
            "eight":8,
            "nine":9,
                }
        first, last = None, None
        first_i, last_i = len(line), 0
        # loop over all digits 1 to 9 and 'one' to 'nine'
        # compute first and last index and keep the current best
        for w in set(digits.keys()) | set(map(str, range(1, 9+1))):
            first_w = line.find(w)
            last_w = line.rindex(w) if first_w >= 0 else len(line)
            if 0 <= first_w < first_i:
                first_i = first_w
                first = digits[w] if w in digits else int(w)
            if last_i < last_w < len(line):
                last_i = last_w
                last = digits[w] if w in digits else int(w)
        return 10*first + (last if last is not None else first)
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
