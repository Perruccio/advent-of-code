import pathlib
import aoc.parse
import aoc

@aoc.pretty_solution(1)
def part1(data):
    def next(i, j, h, w, right):
        next_i = i if right else (i + 1) % h
        next_j = (j + 1) % w if right else j
        return next_i, next_j

    def move(data, h, w, right):
        c = '>' if right else 'v'
        advance = set()
        for i in range(h):
            for j in range(w):
                next_i, next_j = next(i, j, h, w, right)
                if data[i][j] == c and data[next_i][next_j] == '.':
                    advance.add((i, j))
        for (i, j) in advance:
            next_i, next_j = next(i, j, h, w, right)
            data[i][j] = '.'
            data[next_i][next_j] = c
        return data, len(advance) > 0

    h = len(data)
    w = len(data[0])
    i = 0
    while True:
        data, moved_r = move(data, h, w, right=True)
        data, moved_d = move(data, h, w, right=False)
        i += 1
        if not moved_r and not moved_d:
            return i


def main():
    def map_line(line):
        return list(line)

    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)
    return part1(data)
    

def test():
    p1 = main()
    assert p1 == 295


if __name__ == "__main__":
    main()
