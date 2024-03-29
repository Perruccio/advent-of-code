import copy
from collections import deque
from math import prod
from operator import add, attrgetter, mul

from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


class Monkey:
    __slots__ = ("items", "operation", "mod", "get_to", "inspected", "cache")
    # lcm common to every monkey
    # warning: this is very bad modeling of lcm and divide_worry...
    lcm = None
    divide_worry = 1

    def __init__(self, items, operation, mod, get_to):
        self.items = items
        self.operation = operation
        self.mod = mod
        self.get_to = get_to
        self.inspected = 0
        self.cache = {}  # old:new, to

    @classmethod
    def create_monkey(cls, lines):
        # NB assuming a lot about the structure of lines data
        assert len(lines) == 6

        items = deque(aoc_parse.get_ints(lines[1]))
        # parse operation
        operator, val = lines[2].split()[-2:]
        assert operator == "*" or operator == "+"
        op = {"*": mul, "+": add}[operator]
        mod = aoc_parse.get_ints(lines[3])[0]
        to_if_true = aoc_parse.get_ints(lines[4])[0]
        to_if_false = aoc_parse.get_ints(lines[5])[0]
        return cls(
            items,
            lambda old: op(old, old if val == "old" else int(val)),
            mod,
            lambda x: [to_if_false, to_if_true][x % mod == 0],
        )

    def throw(self):
        # take items from left
        old = self.items.popleft()
        self.inspected += 1
        if old not in self.cache:
            # compute new worry level
            new = self.operation(old) // Monkey.divide_worry
            if Monkey.lcm:
                new %= Monkey.lcm
            self.cache[old] = (new, self.get_to(new))
        return self.cache[old]

    def catch(self, item):
        self.items.append(item)


def get_input(file):
    raw = aoc.read_input(2022, 11, file)
    # split in \n\n to get each raw monkey, then split in \n to get lines
    return [Monkey.create_monkey(raw_monkey.split("\n")) for raw_monkey in raw.split("\n\n")]


def solve(monkeys, rounds):
    for _ in range(rounds):
        for monkey in monkeys:
            # use all items for each monkey
            while monkey.items:
                item, to = monkey.throw()
                monkeys[to].catch(item)
    # compute 2 greatest inspections and multiply
    insp1, insp2 = sorted(map(attrgetter("inspected"), monkeys), reverse=True)[:2]
    return insp1 * insp2


@aoc.pretty_solution(1)
def part1(monkeys, rounds=20):
    # NB avoid modifying monkeys, so that part 2 will begin from original state
    monkeys = copy.deepcopy(monkeys)
    Monkey.divide_worry = 3
    return solve(monkeys, rounds)


@aoc.pretty_solution(2)
def part2(monkeys, rounds=10000):
    # not really a lcm
    Monkey.lcm = prod(monkey.mod for monkey in monkeys)
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
