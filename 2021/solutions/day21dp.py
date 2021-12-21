import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

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

def part2(p1, p2):

    max_score = 29
    max_turn = 21
    max_pos = 10

    # possible outcomes of throwing the dice 3 times
    # outcome:frequency
    outcomes = {x:f for x, f in zip(range(3,10), [1,3,6,7,6,3,1])}

    # dp[turn][p1][s1][p2][s2] = number of universes
    dp = [[[[[0
    for _ in range(max_score + 1)]
    for __ in range(max_pos + 1)]
    for ___ in range(max_score + 1)]
    for ____ in range(max_pos + 1)]
    for _____ in range(max_turn + 1)]

    # initial state
    dp[0][p1][0][p2][0] = 1
    
    win1, win2 = 0, 0
    for last_turn in range(0, max_turn):
        for last_p1 in range(1, max_pos + 1):
            for last_s1 in range(max_score + 1):
                for last_p2 in range(1, max_pos + 1):
                    for last_s2 in range(max_score + 1):
                        last_dp = dp[last_turn][last_p1][last_s1][last_p2][last_s2]
                        if last_dp > 0:
                            for outcome1, freq1 in outcomes.items():
                                p1 = (last_p1 + outcome1 - 1) % 10 + 1
                                s1 = last_s1 + p1
                                if s1 >= 21:
                                    win1 += freq1 * last_dp
                                    continue
                                    
                                for outcome2, freq2 in outcomes.items():
                                    p2 = (last_p2 + outcome2 - 1) % 10 + 1
                                    s2 = last_s2 + p2
                                    if s2 >= 21:
                                        win2 += freq2 * last_dp
                                        continue

                                    dp[last_turn + 1][p1][s1][p2][s2] += freq1 * freq2 * last_dp
    return max(win1, win2)

def main(pretty_print = True):
    def map_line(line):
        return int(line.split(': ')[1])
    
    p1, p2 = map_input_lines(prj_path + '/input/day21.txt', map_line)
    
    if (pretty_print):
        print_results(1, part1, p1, p2)
        print_results(2, part2, p1, p2)
    else:
        return part1(p1, p2), part2(p1, p2)
   
if __name__ == "__main__":
    main()