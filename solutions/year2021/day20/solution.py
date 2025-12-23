import pathlib
import aoc.parse
import aoc


def enhance(image, inf, alg):
    def light(pixel, image, inf, alg):
        index = ''
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= pixel[0] + i < len(image) and 0 <= pixel[1] + j < len(image[0]):
                    index += str(image[pixel[0] + i][pixel[1] + j])
                else:
                    index += str(inf)
        return alg[int(index, 2)]

    # new image
    h, w = len(image) + 2, len(image[0]) + 2
    new_image = [[0] * w for _ in range(h)]

    # add padding to old image
    pad_image = [[inf] * w]
    for line in image:
        pad_image += [[inf] + line[:] + [inf]]
    pad_image += [[inf] * w]

    # enhance image
    for i in range(h):
        for j in range(w):
            new_image[i][j] = light((i, j), pad_image, inf, alg)

    return new_image, alg[0 if inf == 0 else -1]


def enhance_n(image, alg, n):
    inf = 0
    for _ in range(n):
        image, inf = enhance(image, inf, alg)
    return sum([sum(line) for line in image])


@aoc.pretty_solution(1)
def part1(image, alg):
    return enhance_n(image, alg, 2)


@aoc.pretty_solution(2)
def part2(image, alg):
    return enhance_n(image, alg, 50)


def main():
    data = aoc.parse.input_as_string(str(pathlib.Path(__file__).parent/'input.txt')).split('\n\n')
    alg = [int(x == '#') for x in data[0]]
    image = [[int(x == '#') for x in line] for line in data[1].split('\n')]
    return part1(image, alg), part2(image, alg)
    

def test():
    p1, p2 = main()
    assert p1 == 4928
    assert p2 == 16605


if __name__ == "__main__":
    main()
