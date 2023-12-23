from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from functools import reduce


def get_input(file):
    return aoc.read_input(2023, 15, file)


def hash256(word):
    def update_hash(h, c):
        return (h + ord(c)) * 17 % 256

    return reduce(update_hash, word, 0)


@aoc.pretty_solution(1)
def part1(data):
    return sum(map(hash256, data.split(",")))


@aoc.pretty_solution(2)
def part2(data):
    # init a vector of boxes to store labels
    hashmap = [[] for _ in range(256)]
    # the focal lengths are stored in a dictionary
    # because there can't be two equal labels with different
    # focal lengths
    focals = {}
    # simulate the process
    for tag in data.split(","):
        label = tag[:-1] if "-" in tag else tag.split("=")[0]
        h = hash256(label)
        if "-" in tag and label in focals:
            # in this case just remove from hashmap and focals
            hashmap[h].remove(label)
            del focals[label]
        elif "=" in tag:
            # add to end if necessary
            if label not in focals:
                hashmap[h].append(label)
            # replace or add
            focals[label] = int(tag.split("=")[-1])

    # compute final score
    res = 0
    for i, box in enumerate(hashmap, 1):
        for j, lens in enumerate(box, 1):
            res += i * j * focals[lens]
    return res


def main():
    data = get_input("example.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 515210
    assert part2(data) == 246762
    print("Test OK")


if __name__ == "__main__":
    test()
