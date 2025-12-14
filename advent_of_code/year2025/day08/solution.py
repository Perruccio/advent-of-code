from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2025, 8, file)
    lines = raw.splitlines()
    return [tuple(map(int, line.split(","))) for line in lines]


def dist(p1, p2):
    return aoc_math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


@aoc.pretty_solution(1)
def part1(data):
    connections = 1000
    comb = list(combinations(range(len(data)), 2))
    dists = sorted(comb, key=lambda ii: dist(data[ii[0]], data[ii[1]]))[:connections]
    circuits = []
    for p1, p2 in dists:
        c1, c2 = map(lambda p: next((i for i in range(len(circuits)) if p in circuits[i]), None), [p1, p2])
        if c1 is not None and c1 == c2:
            continue
        elif c1 is None and c2 is None:
            circuits.append({p1, p2})
        elif c1 is None:
            circuits[c2].add(p1)
        elif c2 is None:
            circuits[c1].add(p2)
        elif c1 is not None and c2 is not None:
            c = circuits[c1] | circuits[c2]
            del circuits[max(c1, c2)]
            del circuits[min(c1, c2)]
            circuits.append(c)
    return prod(sorted(set(map(len, circuits)))[-3:])


@aoc.pretty_solution(2)
def part2(data):
    comb = list(combinations(range(len(data)), 2))
    dists = sorted(comb, key=lambda ii: dist(data[ii[0]], data[ii[1]]))
    circuits = []
    for p1, p2 in dists:
        c1, c2 = map(lambda p: next((i for i in range(len(circuits)) if p in circuits[i]), None), [p1, p2])
        if c1 is not None and c1 == c2:
            continue
        last = p1, p2
        
        if c1 is None and c2 is None:
            circuits.append({p1, p2})
        elif c1 is None:
            circuits[c2].add(p1)
        elif c2 is None:
            circuits[c1].add(p2)
        elif c1 is not None and c2 is not None:
            c = circuits[c1] | circuits[c2]
            del circuits[max(c1, c2)]
            del circuits[min(c1, c2)]
            circuits.append(c)
    return data[last[0]][0] * data[last[1]][0]


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 115885
    assert part2(data) == 274150525
    print("Test OK")


if __name__ == "__main__":
    main()
