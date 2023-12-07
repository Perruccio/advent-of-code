from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from operator import itemgetter

def get_input(file):
    raw = aoc.read_input(2023, 5, file)
    lines = aoc_parse.as_lines(raw)
    seeds = aoc_parse.get_ints(lines[0])
    almanac = []
    for line in lines[2:]:
        if len(line) == 0:
            continue
        if line[0].isalpha():
            almanac.append([])
            continue
        almanac[-1].append(list(map(int, line.split())))
    return seeds, almanac


@aoc.pretty_solution(1)
def part1(seeds, almanac):
    res = float('inf')
    for seed in seeds:
        for map in almanac:
            for dest, src, rng in map:
                if src <= seed < src + rng:
                    seed -= (src - dest)
                    break
        res = min(res, seed)
    return res


@aoc.pretty_solution(2)
def part2(seeds, almanac):
    # basically do the computatin interval by interval
    # cut intervals when an intersection with the map rule is found
    intervals = list(zip(seeds[::2], seeds[1::2]))
    res = float('inf')
    for l, n in intervals:
        # interval of seeds is [l, r)
        curr = [(l, l + n)]
        for map in almanac:
            # new is the vector of new intervals after following the instructions
            # nb the interval can be split after each step
            new = []
            while curr:
                # handle interval [a, b):
                a, b = curr.pop()
                # find all possible intersections with instructions
                for dest, src, rng in map:
                    src_a, src_b = src, src + rng
                    new_a, new_b = max(a, src_a), min(b, src_b)
                    # we have intersection iff new_a < new_b
                    # continue if no intersection
                    if new_a >= new_b:
                        continue
                    delta = src - dest
                    # new interval
                    new.append((new_a - delta, new_b - delta))
                    # take care of what remains (at most 2 intervals).
                    # it can intersect with later instructions so it must be re-added to curr
                    if a < new_a:
                        curr.append((a, new_a))
                    if new_b < b:
                        curr.append((new_b, b))
                    # intersection is found, don't re-add whole interval
                    break
                else:
                    # no intersection found -> interval remains untouched
                    new.append((a, b))
            # update curr with new
            curr = new
        res = min(res, min(map(itemgetter(0), curr)))
    return res


def main():
    seeds, almanac = get_input("input.txt")
    part1(seeds, almanac)
    part2(seeds, almanac)


def test():
    seeds, almanac = get_input("input.txt")
    assert part1(seeds, almanac) == 340994526
    assert part2(seeds, almanac) == 52210644
    print("Test OK")


if __name__ == "__main__":
    main()
