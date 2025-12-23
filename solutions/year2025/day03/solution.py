import aoc


def get_input(file):
    raw = aoc.read_input(2025, 3, file)
    return aoc.parse.as_lines(raw)


@aoc.pretty_solution(1)
def part1(data):
    data = [[int(c) for c in line] for line in data]
    res = 0
    for bank in data:
        # first and second digit of max
        i_mx1, mx1 =  aoc.math.argmax(bank, 0, len(bank)-1)
        mx2 = max(bank[i_mx1+1:])
        res += mx2 + 10*mx1
    return res


@aoc.pretty_solution(2)
def part2(data):
    def max_ndigits(v, n):
        res = []
        # keep track of last inserted index
        left = 0
        for exclude in range(n-1, -1, -1):
            # greedy look for first occurrence of max
            # that leves enough space for other digits
            mx = max(v[left:len(v)-exclude])
            res.append(mx)
            # update left index
            left = v.find(mx, left) + 1
        return res

    res = 0
    for bank in data:
        mx = max_ndigits(bank, 12)
        res += int(''.join(mx))
    return res


def main():
    data = get_input("example.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 17113
    assert part2(data) == 169709990062889
    print("Test OK")


if __name__ == "__main__":
    test()
