from advent_of_code.lib import aoc


def get_input(file):
    return aoc.read_input(2022, 6, file)


def check_different_chars(s):
    return len(set(s)) == len(s)


@aoc.pretty_solution(1)
def part1(input, k=4):
    for i in range(len(input) - k + 1):
        if check_different_chars(input[i : i + k]):
            return i + k
    raise RuntimeError


@aoc.pretty_solution(2)
def part2(input):
    return part1(input, k=14)


def main():
    input = get_input("input.txt")
    part1(input)
    part2(input)


def test():
    input = get_input("input.txt")

    # part 1
    assert part1(input) == 1155
    assert part1("abcd") == 4
    assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    # part 2
    assert part2(input) == 2789
    assert part2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26

    print("Test OK")


if __name__ == "__main__":
    main()
