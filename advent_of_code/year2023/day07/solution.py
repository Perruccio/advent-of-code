from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from collections import Counter
from functools import cmp_to_key


FIGURES = {"T":10, "J":11, "Q":12, "K":13, "A":14}


def get_input(file):
    raw = aoc.read_input(2023, 7, file)
    lines = aoc_parse.as_lines(raw)
    res = []
    for line in lines:
        hand, bid = line.split()
        res.append((hand, int(bid)))
    return res


def compute_point(hand, joker):
    if joker == True:
        mx = 0
        # brute force every possible value of "J"
        for j in set(range(2, 9+1)) | FIGURES.keys():
            new_hand = hand.replace("J", str(j))
            mx = max(mx, compute_point(new_hand, False))
        return mx

    # joker == False
    counts = sorted(Counter(hand).values())
    match counts[-1], (counts[-2] if len(counts) > 1 else None):
        case 5, _: return 7
        case 4, _: return 6
        case 3, 2: return 5
        case 3, 1: return 4
        case 3, 1: return 4
        case 2, 2: return 3
        case 2, 1: return 2
        case 1, _: return 1


def card_value(c, joker):
    return int(c) if c.isdigit() else (1 if c == "J" and joker else FIGURES[c])


def cmp_cards(c1, c2, joker):
    v1, v2 = card_value(c1, joker), card_value(c2, joker)
    return (v1 > v2) - (v1 < v2)


def cmp_hands(h1, h2, joker=False):
    p1, p2 = compute_point(h1, joker), compute_point(h2, joker)
    # winner is the one with higher point
    if p1 != p2:
        return -1 if p1 < p2 else 1
    if h1 == h2:
        return 0
    # otherwise check card by card
    for c1, c2 in zip(h1, h2):
        res = cmp_cards(c1, c2, joker)
        if res != 0:
            return res
    return 0


@aoc.pretty_solution(1)
def part1(data):
    # given a couple (hand, bid), order by hand using cmp_hands as compare function
    data.sort(key=lambda pair: cmp_to_key(cmp_hands)(pair[0]))
    return sum(i * bid for i, (hand,  bid) in enumerate(data, 1))


@aoc.pretty_solution(2)
def part2(data):
    data.sort(key=lambda pair: cmp_to_key(lambda q1, q2:cmp_hands(q1, q2, True))(pair[0]))
    return sum(i * bid for i, (hand,  bid) in enumerate(data, 1))


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 248812215
    assert part2(data) == 250057090
    print("Test OK")


if __name__ == "__main__":
    main()
