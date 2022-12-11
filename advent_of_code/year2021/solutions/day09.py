import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse
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

def main(pretty_print = True):
    def map_line(line):
        return [int(x) for x in line]

    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day09.txt', map_line)

    if (pretty_print):
        aoc_output.print_result(1, part1, data)
        aoc_output.print_result(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()
