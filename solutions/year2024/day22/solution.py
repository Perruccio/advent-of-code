from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2024, 22, file)
    return aoc.parse.get_ints(raw)


def step(n, P, times = 1):
    # just do every step as described
    for _ in range(times):
        n = n^(n << 6) % P
        n = n^(n >> 5) % P
        n = n^(n << 11) % P
    return n


@aoc.pretty_solution(1)
def part1(nums):
    P = 16777216
    return sum(map(lambda n: step(n, P, 2000), nums))


@aoc.pretty_solution(2)
def part2(nums):
    P = 16777216
    # keep a dictionary with total amount of bananas for each sequence
    seqs = defaultdict(int)
    for n in nums:
        # keep track of all changes
        changes = []
        # keep track of seen sequence of 4 changes, because
        # we only count the first one it appears
        seen = set()
        for i in range(2000):
            # old price
            old = n % 10
            n = step(n, P)
            changes.append(n%10 - old)
            if i >= 3:
                # add n of bananas we would get from this monkey
                # with this sequence
                seq = tuple(changes[-4:])
                if seq not in seen:
                    seqs[seq] += n%10
                    seen.add(seq)
    return max(seqs.values())


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 14726157693
    assert part2(data) == 1614
    print("Test OK")


if __name__ == "__main__":
    test()
