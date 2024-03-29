from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2022, 2, file)
    return aoc_parse.map_by_line(raw, lambda line: line.split())


def decrypt_opponent(opp):
    """modulo 3 moves: rock = 0, paper = 1, scissors = 2"""
    return ord(opp) - ord("A")


def rock_paper_scissors(player, opponent):
    """
    return 'win'/'draw'/'loss' from player's perspective
    use modulo 3 arithmetic, 0 < 1 < 2 < 0
    """
    # 'draw' if player == opponent, 'win' if player = opponent + 1,
    # lose if player == opponent-1 (mod3) (in this case player - opponent = -1 = 2)
    return ["draw", "win", "loss"][(player - opponent) % 3]


def round_score(player, opponent):
    """shape points + outcome points"""
    # rock:1, paper:2, scissors:3
    shape_points = {0: 1, 1: 2, 2: 3}
    outcome_points = {"win": 6, "draw": 3, "loss": 0}
    return shape_points[player] + outcome_points[rock_paper_scissors(player, opponent)]


@aoc.pretty_solution(1)
def part1(v):
    def decrypt_player(pl):
        return ord(pl) - ord("X")

    return sum([round_score(decrypt_player(pl), decrypt_opponent(opp)) for opp, pl in v])


@aoc.pretty_solution(2)
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


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 8890
    assert part2(data) == 10238
    print("Test OK")


if __name__ == "__main__":
    test()
