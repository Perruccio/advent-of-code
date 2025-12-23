from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2024, 2, file)
    return aoc.parse.map_by_line(raw, aoc.parse.get_ints)


def safe(line):
    s = aoc.math.sign(line[1] - line[0])
    for a, b in zip(line, line[1:]):
        if abs(a-b) < 1 or abs(a-b) > 3:
            return False
        if aoc.math.sign(b - a) != s:
            return False
    return True

def almost_safe(line):
    if safe(line):
        return True
    return any(safe(line[:i] + line[i+1:]) for i in range(0, len(line)))

@aoc.pretty_solution(1)
def part1(data):
    return sum(map(safe, data))


@aoc.pretty_solution(2)
def part2(data):
    return sum(map(almost_safe, data))


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 606
    assert part2(data) == 644
    print("Test OK")


if __name__ == "__main__":
    test()
