from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    return aoc_parse.as_lines(aoc.read_input(2022, 25, file))


def to_snafu(n):
    # snafu replaces 3 with its mod5 equivalent -2 and 4 with -1 (works fine because we still
    # get a set of 5 values wich are equivalent to 0,1,2,3,4 mod5).
    # Conversion is easy when we see that we must write n = s0 * 5^0 + s1 * 5^1 + ...
    # where s_i are snafu digits. To find s0 just compute n%5: if we get 0,1,2 then just use
    # standard conversion, otherwise say we got 3 and need to replace it with -2: we need to add 5
    # to restore equality, i.e. n = 3 + s1 * 5 + ... = (5 - 2) + s1 * 5 + ...
    # n = -2 + (s1 + 1) * 5 + ... Which means that if the remainder is 3 or 4, we need to add the
    # carry to the next digit: to do this, we could simply add 1 to n after n//=5
    # (this is the used way below).
    # Another way of doing it would be to realize that n - s0 = s1 * 5 + ... hence we could simply
    # subtract s0 from n and then do //5. This works because if s0 is negative, it will
    # automatically add the carry to n, and would be harmless if positive:
    # E.g. n = 8, (n + 2)%5 - 2 = -2 (first digit from right), then 8 - (-2) = 10 and 10//5 = 2
    # and continue until n=0 -> (2 + 2) % 5 - 2 = 2 (second digit from right), then 2-2 =0 stop
    # result is "2="
    snafu_number = ""
    while n:
        n, rem = divmod(n, 5)
        snafu_number = "012=-"[rem] + snafu_number
        # add carry to next digit by incrementing n by 1 (if necessary) after // 5
        n += rem > 2
    return snafu_number


def snafu_to_dec(x):
    decimal_digits = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
    # standard change of base to decimal, just do c0 * 5^0 + c1 * 5^ 1 + ...
    # = sum_{i=0}^{n digits} c_i * 5 ^ i
    return sum(decimal_digits[c] * 5**i for i, c in enumerate(x[::-1]))


@aoc.pretty_solution(1)
def part1(data):
    return to_snafu(sum(map(snafu_to_dec, data)))


def main():
    data = get_input("input.txt")
    part1(data)


def test():
    assert snafu_to_dec("1-0---0") == 12345
    assert snafu_to_dec("1121-1110-1=0") == 314159265

    example = get_input("input.txt")
    assert part1(example) == "122-12==0-01=00-0=02"

    print("Test OK")


if __name__ == "__main__":
    test()
