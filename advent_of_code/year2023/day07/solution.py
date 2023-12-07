from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from collections import Counter
from functools import cmp_to_key


def get_input(file):
    raw = aoc.read_input(2023, 7, file)
    lines = aoc_parse.as_lines(raw)
    res = []
    for line in lines:
        hand, bid = line.split()
        # NB trick from some redditor:
        # - first notice that the point of the hand can be expressed
        #   by its sorted counter
        # - second, take care of the tie with alphabetical comparison
        #   it suffices to replace TJQKA with ABCDE because in ASCII
        #   '2' < ... < '9' < 'A' < .. < 'E'
        res.append((hand.translate(str.maketrans('TJQKA', 'ABCDE')), int(bid)))
    return res


def compute_point(hand, joker):
    if joker == True:
        mx = [], ""
        # NB remember that in case of ties, "J" (now "B") is the lowest
        # replace it with "0"
        # brute force every possible value of "J" (now "B")
        for j in set(range(2, 9+1)) | set("ACDE"):
            new_hand = hand.replace("B", str(j))
            point = compute_point(new_hand, False)[0], hand.replace("B", "0")
            mx = max(mx, point)
        return mx

    # joker == False
    return sorted(Counter(hand).values(), reverse=True), hand


@aoc.pretty_solution(1)
def part1(data):
    # given a couple (hand, bid), order by hand using cmp_hands as compare function
    data.sort(key=lambda pair: compute_point(pair[0], False))
    return sum(rank * bid for rank, (hand,  bid) in enumerate(data, 1))


@aoc.pretty_solution(2)
def part2(data):
    data.sort(key=lambda pair: compute_point(pair[0], True))
    return sum(rank * bid for rank, (hand,  bid) in enumerate(data, 1))


def main():
    data = get_input("example.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 248812215
    assert part2(data) == 250057090
    print("Test OK")


if __name__ == "__main__":
    test()
