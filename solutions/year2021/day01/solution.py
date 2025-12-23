import pathlib
import aoc.parse
import aoc


@aoc.pretty_solution(1)
def part1(v):
    return sum(map(int.__lt__, v, v[1:]))


@aoc.pretty_solution(2)
def part2(v, shift=3):
    return sum(map(int.__lt__, v, v[shift:]))


def main():
    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), int)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 1709
    assert p2 == 1761


if __name__ == "__main__":
    main()
