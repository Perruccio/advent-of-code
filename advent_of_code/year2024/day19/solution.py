from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 19, file)
    tokens, words = raw.split("\n\n")
    tokens = tokens.split(", ")
    words = words.split("\n")
    return set(tokens), words


def count(tokens, word):
    dp = [word[:i+1] in tokens for i in range(len(word))]
    for i in range(len(word)):
        dp[i] += sum(dp[j] for j in range(i) if word[j+1:i+1] in tokens)
    return dp[-1]


@aoc.pretty_solution(1)
def part1(tokens, words):
    return sum(map(lambda word: count(tokens, word) > 0, words))


@aoc.pretty_solution(2)
def part2(tokens, words):
    return sum(map(lambda word: count(tokens, word), words))
    # @cache
    # def count_memo(word):
    #     if not word:
    #         return 1
    #     return sum(count_memo(word.removeprefix(token)) for token in tokens if word.startswith(token))
    # return sum(map(count_memo, words))


def test():
    data = get_input("input.txt")
    assert part1(*deepcopy(data)) == 242
    assert part2(*data) == 595975512785325
    print("Test OK")


if __name__ == "__main__":
    test()
