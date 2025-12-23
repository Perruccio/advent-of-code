from aoc.all import *

# to use cache in count
graph = {}

def get_input(file):
    raw = aoc.read_input(2025, 11, file)
    for line in raw.splitlines():
        src, dests = line.split(":")
        graph[src] = list(dests.split())
    return graph


@cache
def count(src, dest):
    # count n of paths from src to dest
    if src == dest:
        return 1
    return sum(count(v, dest) for v in graph[src]) if src in graph else 0


@aoc.pretty_solution(1)
def part1(data):
    return count("you", "out")


@aoc.pretty_solution(2)
def part2(data):
    res = count("svr", "fft") * count("fft", "dac") * count("dac", "out")
    res += count("svr", "dac") * count("dac", "fft") * count("fft", "out")
    return res


def main():
    data = get_input("input.txt")
    part1(deepcopy(data))
    part2(deepcopy(data))


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 534
    assert part2(deepcopy(data)) == 499645520864100
    print("Test OK")


if __name__ == "__main__":
    test()
