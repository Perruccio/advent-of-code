from advent_of_code.lib.all import *


def get_input(file):
    reg, prog = aoc.read_input(2024, 17, file).split("\n\n")
    reg = aoc_parse.get_ints(reg)
    prog = aoc_parse.get_ints(prog)
    return reg, prog


def combo(reg, o):
    if 0 <= o <= 3:
        return o
    return reg[o-4]


@aoc.pretty_solution(1)
def part1(reg, prog):
    i = 0
    res = []
    while i < len(prog):
        p, o = prog[i], prog[i+1]
        i += 2
        if p == 0:
            reg[0] = reg[0] // (2**combo(reg, o))
        elif p == 1:
            reg[1] ^= o
        elif p == 2:
            reg[1] = combo(reg, o)%8
        elif p == 3 and reg[0] != 0:
            i = o
        elif p == 4:
            reg[1] ^= reg[2]
        elif p == 5:
            res.append(combo(reg, o)%8)
        elif p == 6:
            raise
            reg[1] = reg[0] // (2**combo(reg, o))
        elif p == 7:
            reg[2] = reg[0] // (2**combo(reg, o))
        
    return ','.join(map(str, res))

@aoc.pretty_solution(2)
def part2(data):
    return


def test():
    data = get_input("input.txt")
    assert part1(*deepcopy(data)) == "1,5,3,0,2,5,2,5,3"
    # assert part2(data) == 
    part2(data)
    print("Test OK")


if __name__ == "__main__":
    test()
