from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2025, 1, file)
    def parse(line):
        return line[0], int(line[1:])
    return aoc.parse.map_by_line(raw, parse)
    

@aoc.pretty_solution(1)
def part1(data):
    dial = 50
    res = 0
    for dir, steps in data:
        sign = 1 if dir == "R" else -1
        dial = (dial + sign*steps) % 100
        if dial == 0:
            res += 1
    return res


@aoc.pretty_solution(2)
def part2(data):
    dial = 50
    res = 0
    for dir, steps in data:
        # whole loops + remainder
        n_0, rem = divmod(steps, 100)
        sign = 1 if dir == "R" else -1
        new_dial = dial + sign*rem
        # add whole loops
        res += n_0
        # if R, add 1 if >=100. if L, add if <= 0 but
        # remove case where dial was already 0
        res += (dial != 0 and new_dial <= 0) or new_dial >= 100
        dial = new_dial % 100
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 1007
    assert part2(data) == 5820
    print("Test OK")


if __name__ == "__main__":
    test()
