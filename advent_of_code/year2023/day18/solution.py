from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 18, file)
    def read_line(line):
        dig_dir, l, color = line.split(" ")
        return (dig_dir, int(l), color[2:-1])
    return aoc_parse.map_by_line(raw, func=read_line)


def solve(data):
    curr = 0
    area = 0
    perimeter = 0
    for dig, l in data:
        dd = {"D":1j, "R": 1, "L": -1, "U":-1j}[dig]
        # Green's theorem!!
        area += curr.real * dd.imag * l
        curr += dd * l
        perimeter += l
    # NB our grid points are squares with width, not really points.
    # We can see the points as the centers of the squares. This means
    # that the area computed is missing a strip of width 1/2 along the perimeter.
    # The area of this strip is computed by adding the small segment along the perimeter
    # of width 1/2 + 1/4 of the 4 angles
    return area + perimeter // 2 + 1


@aoc.pretty_solution(1)
def part1(data):
    return solve((dig, l) for dig, l, _ in data)


@aoc.pretty_solution(2)
def part2(data):
    return solve(("RDLU"[int(hex[-1])], int(hex[:-1], 16)) for _, _, hex in data)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 49061
    assert part2(data) == 92556825427032
    print("Test OK")


if __name__ == "__main__":
    test()
