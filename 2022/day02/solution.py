import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils.aoc import *


decrypt_opponent = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}

shape_points = {"rock": 1, "paper": 2, "scissors": 3}

outcome_points = {"win": 6, "draw": 3, "loss": 0}

beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}


def rock_paper_scissors(player, opponent):
    # return 'win'/'draw'/'loss' from player's perspective
    if player == opponent:
        return "draw"
    return "win" if beats[player] == opponent else "loss"


def round_score(player, opponent):
    # shape points + outcome points
    return shape_points[player] + outcome_points[rock_paper_scissors(player, opponent)]


def part1(v):
    decrypt_player = {"X": "rock", "Y": "paper", "Z": "scissors"}
    return sum([round_score(decrypt_player[pl], decrypt_opponent[opp]) for opp, pl in v])


def part2(v):
    decrypt_strategy = {"X": "lose", "Y": "draw", "Z": "win"}

    def compute_move(strategy, opponent):
        if strategy == "draw":
            return opponent
        elif strategy == "lose":
            return beats[opponent]
        else:
            return {beats[winner]: winner for winner in beats}[opponent]

    return sum(
        [
            round_score(
                compute_move(decrypt_strategy[pl_strat], decrypt_opponent[opp]),
                decrypt_opponent[opp],
            )
            for opp, pl_strat in v
        ]
    )


def get_input():
    return map_input_lines(str(curr_dir) + "/input.txt", lambda line: line.split())


def main(pretty_print=False):
    data = get_input()
    if pretty_print:
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main(pretty_print=True)
