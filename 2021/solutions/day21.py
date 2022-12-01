import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
from functools import lru_cache, reduce
from itertools import product
from collections import Counter

def part1(p1, p2):
    def play(p, dice, rolls):
        p = (p + 3 * dice - 1) % 10 + 1
        dice = (dice + 3 - 1) % 100 + 1
        rolls += 3
        return p, dice, rolls

    dice, rolls = 2, 0
    s1, s2 = 0, 0
    while True:
        p1, dice, rolls = play(p1, dice, rolls)
        s1 += p1
        if s1 >= 1000:
            winner = 1
            break
        p2, dice, rolls = play(p2, dice, rolls)
        s2 += p2
        if s2 >= 1000:
            winner = 2
            break

    return rolls * (s1 if winner == 2 else s2)

OUTCOMES = Counter(map(sum, product(*[[1,2,3]]*3)))

@lru_cache(maxsize=None)
def quantum_dice(p1, s1, p2, s2):
    # p1 is current player
    if s1 >= 21:
        return 1, 0
    if s2 >= 21:
        return 0, 1

    win1 = win2 = 0
    for outcome, freq in OUTCOMES.items():
        p1_new = (p1 + outcome - 1) % 10 + 1
        s1_new = s1 + p1_new
        # switch players!
        next_win2, next_win1 = quantum_dice(p2, s2, p1_new, s1_new)
        win1 += next_win1 * freq
        win2 += next_win2 * freq
    return win1, win2

def part2(p1, p2):
    return max(quantum_dice(p1, 0, p2, 0))

def main(pretty_print = True):
    def map_line(line):
        return int(line.split(': ')[1])

    p1, p2 = map_input_lines(prj_path + '/2021/input/day21.txt', map_line)

    if (pretty_print):
        print_results(1, part1, p1, p2)
        print_results(2, part2, p1, p2)
    else:
        return part1(p1, p2), part2(p1, p2)

if __name__ == "__main__":
    main()