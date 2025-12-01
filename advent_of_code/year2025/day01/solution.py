from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2025, 1, file)
    def parse(line):
        return line[0], int(line[1:])
    return aoc_parse.map_by_line(raw, parse)
    

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
    def count(a, b, n):
        """count how many multiples of n are between (a, b]"""
        sign = 1 if b > a else -1
        res = 0
        for i in range(a+sign, b+sign, sign):
            if i%n ==0:
                res +=1
        return res

    dial = 50
    res = 0
    for dir, steps in data:
        sign = 1 if dir == "R" else -1
        new_dial = dial + sign*steps
        res += count(dial, new_dial, 100)
        dial = (new_dial) % 100
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
