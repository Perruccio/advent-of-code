import pathlib

import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse


def get_input(file):
    return aoc_parse.input_as_string(str(pathlib.Path(__file__).parent) + "/" + file)


def check_different_chars(s):
    return len(set(s)) == len(s)


def part1(input, k=4):
    for i in range(len(input) - k + 1):
        if check_different_chars(input[i : i + k]):
            return i + k
    raise RuntimeError


def part2(input):
    return part1(input, k=14)


def main():
    input = get_input("input.txt")
    aoc_output.print_result(1, part1, input)
    aoc_output.print_result(2, part2, input)


def test():
    input = get_input("input.txt")

    # part 1
    assert part1(input) == 1155
    assert part1("abcd") == 4
    assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    #part 2
    assert part2(input) == 2789
    assert part2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26
    
    print("Test OK")


if __name__ == "__main__":
    main()
