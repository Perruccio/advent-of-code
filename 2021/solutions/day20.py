import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def enhance(image, inf, alg):
    def light(pixel, image, inf, alg):
        index = ''
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= pixel[0] + i < len(image) and 0 <= pixel[1] + j < len(image[0]):
                    index += str(image[pixel[0]+i][pixel[1]+j])
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

def part1(image, alg):
    return enhance_n(image, alg, 2)

def part2(image, alg):
    return enhance_n(image, alg, 50)

def main(pretty_print = True):
    data = input_as_string(prj_path + '/2021/input/day20.txt').split('\n\n')
    alg = [int(x == '#') for x in data[0]]
    image = [[int(x == '#') for x in line] for line in data[1].split('\n')]

    if (pretty_print):
        print_results(1, part1, image, alg)
        print_results(2, part2, image, alg)
    else:
        return part1(image, alg), part2(image, alg)

if __name__ == "__main__":
    main()