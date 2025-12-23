import pathlib
import aoc.parse
import aoc


@aoc.pretty_solution(1)
def part1(data):
    horizontal = sum(x[1] for x in data if x[0] == 'forward')
    depth = sum(
        -x[1] if x[0] == 'up' else
        x[1] if x[0] == 'down' else
        0
        for x in data)
    return horizontal * depth


@aoc.pretty_solution(2)
def part2(data):
    h_pos = 0
    d_pos = 0
    aim = 0
    for dir, step in data:
        if dir == "down":
            aim += step
        elif dir == "up":
            aim -= step
        elif dir == "forward":
            h_pos += step
            d_pos += aim * step
    return h_pos * d_pos


def main():
    def map_line(line):
        a, b = line.split()
        return a, int(b)

    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 2117664
    assert p2 == 2073416724


if __name__ == "__main__":
    main()
