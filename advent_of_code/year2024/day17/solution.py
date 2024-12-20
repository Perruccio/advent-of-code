from advent_of_code.lib.all import *


def get_input(file):
    reg, prog = aoc.read_input(2024, 17, file).split("\n\n")
    reg = aoc_parse.get_ints(reg)
    prog = aoc_parse.get_ints(prog)
    return reg, prog


@aoc.pretty_solution(1)
def part1(reg, prog):
    def combo(o):
        if 0 <= o <= 3:
            return o
        return [a, b, c][o-4]

    a, b, c = reg
    i, res = 0, []
    while i < len(prog):
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
            raise
            b = a // (2**combo(o))
        elif p == 7:
            c = a // (2**combo(o))
        
    return ','.join(map(str, res))

@aoc.pretty_solution(2)
def part2(reg, prog):
    for i in range(0, len(prog), 2):
        print(prog[i], prog[i+1])
    return


def test():
    data = get_input("input.txt")
    assert part1(*deepcopy(data)) == "1,5,3,0,2,5,2,5,3"
    # assert part2(data) == 
    part2(*data)
    print("Test OK")


if __name__ == "__main__":
    # test()
    data = get_input("test.txt")
    for a in range(0, 8):
        print(f"{a=}")
        part1([a, 0, 0], data[1])
