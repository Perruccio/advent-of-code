import pathlib
import aoc.parse
import aoc
from math import prod


def get_neighbours(end_i, end_j, pos):
    # return coordinates of 4 neighbours (no diagonal)
    i, j = pos
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        i2, j2 = i + di, j + dj
        if 0 <= i2 < end_i and 0 <= j2 < end_j:
            yield i2, j2


def low_points(data):
    # return list of low points (local minima)
    end_i, end_j = len(data), len(data[0])
    for i in range(len(data)):
        for j in range(len(data[i])):
            if all([data[i2][j2] > data[i][j] for i2, j2 in get_neighbours(end_i, end_j, (i, j))]):
                yield i, j


@aoc.pretty_solution(1)
def part1(data):
    return sum([data[i][j] + 1 for i, j in low_points(data)])


# part 2 with (kind of) breadth first search
def part2(data):
    end_i, end_j = len(data), len(data[0])
    basin_size = []
    for low in low_points(data):
        visited = set()
        frontier = {low}
        # continue adding neighbours (horiz/vert) to frontier until 9 is found
        while frontier:
            pos = frontier.pop()
            if pos not in visited:
                visited.add(pos)
                for i2, j2 in get_neighbours(end_i, end_j, pos):
                    if (i2, j2) not in visited and data[i2][j2] < 9:
                        frontier.add((i2, j2))
        basin_size.append(len(visited))

    return prod(sorted(basin_size)[-3:])


@aoc.pretty_solution(2)
def part22(data):
    end_i, end_j = len(data), len(data[0])

    def expand(data, i, j, visited):
        """ return size of basin that includes i, j """
        basin_size = 0
        if (i, j) not in visited and data[i][j] < 9:
            visited.add((i, j))
            basin_size += 1
            for i1, j2 in get_neighbours(end_i, end_j, (i, j)):
                basin_size += expand(data, i1, j2, visited)
        return basin_size

    visited = set()
    basins_size = [expand(data, i, j, visited) for i in range(end_i) for j in range(end_j) if (i, j) not in visited]
    return prod(sorted(basins_size)[-3:])


def main():
    def map_line(line):
        return [int(x) for x in line]

    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 532
    assert p2 == 1110780


if __name__ == "__main__":
    main()
