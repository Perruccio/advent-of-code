import pathlib
import advent_of_code.utils.aoc as aoc
from collections import deque
import re
import copy
from functools import reduce


class Monkey:
    # mcm common to every monkey
    mcm = None
    divide_worry = 1

    def __init__(self, items, operation, mod, get_to):
        self.items = items
        self.operation = operation
        self.mod = mod
        self.get_to = get_to
        self.inspected = 0
        self.cache = {}  # old:new, to

    @staticmethod
    def create_monkey(raw):
        # NB assuming a lot about the structure of raw data
        assert len(raw) == 6
        items = deque(map(int, re.findall(aoc.RE["int"], raw[1])))
        operation = eval("lambda old : " + raw[2][len("  Operation: new = ") :])
        mod = int(raw[3].split()[-1])
        to_if_true = int(raw[4].split()[-1])
        to_if_false = int(raw[5].split()[-1])
        return Monkey(items, operation, mod, lambda x: [to_if_false, to_if_true][x % mod == 0])

    def throw(self):
        # take items from left
        old = self.items.popleft()
        self.inspected += 1
        if old not in self.cache:
            # compute new worry level
            new = self.operation(old) // Monkey.divide_worry
            if Monkey.mcm:
                new %= Monkey.mcm
            self.cache[old] = (new, self.get_to(new))
        return self.cache[old]

    def catch(self, item):
        self.items.append(item)


def get_input(file):
    raw = aoc.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)
    return [Monkey.create_monkey(raw[i : i + 6]) for i in range(0, len(raw), 7)]


def solve(monkeys, rounds):
    for _ in range(rounds):
        for monkey in monkeys:
            # use all items for each monkey
            while monkey.items:
                item, to = monkey.throw()
                monkeys[to].catch(item)
    # compute 2 greatest inspections and multiply
    most_inspection = sorted([monkey.inspected for monkey in monkeys], reverse=True)[:2]
    return most_inspection[0] * most_inspection[1]


@aoc.pretty_solution(1)
def part1(monkeys, rounds=20):
    # NB avoid modifying monkeys, so that part 2 will begin from original state
    monkeys = copy.deepcopy(monkeys)
    Monkey.divide_worry = 3
    return solve(monkeys, rounds)


@aoc.pretty_solution(2)
def part2(monkeys, rounds=10000):
    Monkey.mcm = reduce(lambda m1, m2: m1 * m2, (monkey.mod for monkey in monkeys))
    Monkey.divide_worry = 1
    return solve(monkeys, rounds)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 10605
    assert part2(example) == 2713310158

    data = get_input("input.txt")
    assert part1(data) == 61005
    assert part2(data) == 20567144694

    print("Test OK")


if __name__ == "__main__":
    test()
