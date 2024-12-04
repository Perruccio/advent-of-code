from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 4, file)
    return aoc_parse.as_lines(raw)


def count_word_grid(grid, i0, j0, word):
    m, n = len(grid), len(grid[0])
    res = 0
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == dj == 0:
                continue
            i, j, c = i0, j0, 0
            while 0 <= i < m and 0 <= j < n and c < len(word) and grid[i][j] == word[c]:
                i += di
                j += dj
                c += 1
            if c == len(word):
                res += 1
    return res


@aoc.pretty_solution(1)
def part1(data):
    m, n = len(data), len(data[0])
    return sum(count_word_grid(data, i, j, "XMAS") for i in range(m) for j in range(n))


@aoc.pretty_solution(2)
def part2(data):
    m, n = len(data), len(data[0])
    def check(i, j):
        if i == 0 or i == m-1 or j == 0 or j == n-1:
            return False
        if data[i][j] != "A":
            return False
        d1 = set([data[i+1][j+1], data[i-1][j-1]])
        d2 = set([data[i+1][j-1], data[i-1][j+1]])
        return d1 == d2 == {"M", "S"}
    return sum(check(i, j) for i in range(m) for j in range(n))


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 2370
    assert part2(data) == 1908
    print("Test OK")


if __name__ == "__main__":
    test()
