import aoc.parse
from aoc import aoc


def get_input(file):
    raw = aoc.read_input(2023, 4, file)
    return aoc.parse.as_lines(raw)


def get_matches(line):
    win, my = map(aoc.parse.get_ints, line.split(":")[1].split("|"))
    return len(set(win) & set(my))


@aoc.pretty_solution(1)
def part1(data):
    res = 0
    for line in data:
        if (matches := get_matches(line)) > 0:
            res += 2**(matches - 1)
    return res


@aoc.pretty_solution(2)
def part2(data):
    # keep state vector
    # cards[i] = how many i-th cards I (currently) have
    cards = [1] * len(data)
    for i, line in enumerate(data):
        matches = get_matches(line)
        # for every card in the next matches cards,
        # add one for each of current i-th card
        for j in range(i + 1, i + matches + 1):
            cards[j] += cards[i]
    return sum(cards)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 24848
    assert part2(data) == 7258152
    print("Test OK")


if __name__ == "__main__":
    main()
