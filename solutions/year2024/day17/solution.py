from aoc.all import *


def get_input(file):
    reg, prog = aoc.read_input(2024, 17, file).split("\n\n")
    reg = aoc.parse.get_ints(reg)
    prog = aoc.parse.get_ints(prog)
    return reg, prog


def compute_generic(reg, prog):
    def combo(o):
        if 0 <= o <= 3:
            return o
        return [a, b, c][o-4]
    a,b,c = reg
    i, res = 0, []
    while i+1 < len(prog):
        p, o = prog[i], prog[i+1]
        i += 2
        if p == 0:
            a = a // (2**combo(o))
        elif p == 1:
            b ^= o
        elif p == 2:
            b = combo(o)%8
        elif p == 3 and a != 0:
            i = o
        elif p == 4:
            b ^= c
        elif p == 5:
            res.append(combo(o)%8)
        elif p == 6:
            b = a // (2**combo(o))
        elif p == 7:
            c = a // (2**combo(o))
    return res


def my_compute(a):
    # hard-coded version of my input program
    res = []
    while 1:
        b = (a%8)^3
        b = (b^(a>>b)^3)%8
        a = a//8
        res.append(b)
        if a == 0:
            break
    return res


@aoc.pretty_solution(1)
def part1(reg, prog):
    return ','.join(map(str, compute_generic(reg, prog)))


@aoc.pretty_solution(2)
def part2(prog):
    # the output takes the last 3 bits of A each time
    # and discard them after. so we basically just need to
    # brute force 3 bits at a time.
    # start with last digit of the target program:
    # we find the set of candidate 3-bit numbers that output this digit:
    # e.g. last digit of target is 0 -> candidates = {0, 3}
    # so we know for sure that the answer for A starts with 000 or 011
    # then, for each of this candidate, we brute-force the next (on the right)
    # 3-bit number that (together with the candidate) outputs the last 2 digits
    # of the program. e.g.  then we try '000' & bin(x) for x in (0,...,7) (3 bits)
    # and '011' & bin(x)
    candidates = {0}
    # start from end of target program
    for i in range(len(prog)-1, -1, -1):
        # brute force
        candidates_new = set()
        for candidate in candidates:
            # find new 3-bit number that matches tail of target program
            for x in range(8):
                a = (candidate << 3) + x
                if my_compute(a) == prog[i:]:
                    candidates_new.add(a)
        candidates = candidates_new
    return min(candidates)


def test():
    reg, program = get_input("input.txt")
    assert part1(reg, program) == "1,5,3,0,2,5,2,5,3"
    assert part2(program) == 108107566389757
    print("Test OK")


if __name__ == "__main__":
    test()
