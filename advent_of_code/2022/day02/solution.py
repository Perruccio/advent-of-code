import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils import aoc

# rock:1, paper:2, scissors:3
shape_points = {0: 1, 1: 2, 2: 3}

outcome_points = {"win": 6, "draw": 3, "loss": 0}


def decrypt_opponent(opp):
    """modulo 3 moves: rock = 0, paper = 1, scissors = 2"""
    return ord(opp) - ord("A")


def rock_paper_scissors(player, opponent):
    """
    return 'win'/'draw'/'loss' from player's perspective
    use modulo 3 arithmetic, 0 < 1 < 2 < 0
    """
    #'draw' if player == opponent, 'win' if player = opponent + 1,
    #lose if player == opponent-1 (mod3) (in this case player - opponent = -1 = 2)
    return ["draw", "win", "loss"][(player - opponent) % 3]


def round_score(player, opponent):
    """ shape points + outcome points """
    return shape_points[player] + outcome_points[rock_paper_scissors(player, opponent)]


def part1(v):
    decrypt_player = lambda pl: ord(pl) - ord("X")
    return sum([round_score(decrypt_player(pl), decrypt_opponent(opp)) for opp, pl in v])


def part2(v):
    def compute_move(strategy, opponent):
        # return (opponent + ord(strategy) - ord("Y")) % 3
        if strategy == "Y":
            return opponent
        elif strategy == "X":
            return (opponent - 1) % 3
        else:
            return (opponent + 1) % 3

    return sum(
        [
            round_score(
                compute_move(pl_strat, decrypt_opponent(opp)),
                decrypt_opponent(opp),
            )
            for opp, pl_strat in v
        ]
    )


def get_input():
    return aoc.map_input_lines(str(curr_dir) + "/input.txt", lambda line: line.split())


def main():
    data = get_input()
    return (aoc.print_result(1, part1, data),
            aoc.print_result(2, part2, data))


def test():
    """test for pytest"""
    assert main() == (8890, 10238)


if __name__ == "__main__":
    main()
