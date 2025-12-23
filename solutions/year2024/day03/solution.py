from aoc.all import *


def get_input(file):
    return aoc.read_input(2024, 3, file)


@aoc.pretty_solution(1)
def part1(data):
    ints = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
    return sum(int(a)*int(b) for a, b in ints)


@aoc.pretty_solution(2)
def part2(data):
    tokens = re.findall(r"mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)", data)
    res = 0
    do = True
    for token in tokens:
        if token == "don't()":
            do = False
        elif token == "do()":
            do = True
        elif do:
            x, y = re.findall(r"\d+", token)
            res += int(x)*int(y)
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 187825547
    assert part2(data) == 85508223
    print("Test OK")


if __name__ == "__main__":
    test()
