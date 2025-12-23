import aoc.parse
from aoc import aoc
from functools import lru_cache


def get_input(file):
    raw = aoc.read_input(2023, 12, file)

    def read_line(line):
        spring, groups = line.split(" ")
        return spring, tuple(map(int, groups.split(",")))

    return aoc.parse.map_by_line(raw, read_line)


@lru_cache
def count(spring, target):
    if not spring or not target:
        return 0 if (target or "#" in spring) else 1
    match spring[0]:
        case ".":
            # just skip
            return count(spring[1:], target)
        case "#":
            # make one whole block at a time (not a single character)
            # be careful because "#" can't be immediately after the block
            if (
                len(spring) < target[0]
                or "." in spring[: target[0]]
                or (len(spring) > target[0] and spring[target[0]] == "#")
            ):
                return 0
            return count(spring[target[0] + 1 :], target[1:])
        case "?":
            # duplicate the string
            return count("#" + spring[1:], target) + count("." + spring[1:], target)


@aoc.pretty_solution(1)
def part1(data):
    return sum(count(spring, target) for spring, target in data)


@aoc.pretty_solution(2)
def part2(data):
    return sum(count("?".join([spring] * 5), target * 5) for spring, target in data)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 7490
    assert part2(data) == 65607131946466
    print("Test OK")


if __name__ == "__main__":
    test()
