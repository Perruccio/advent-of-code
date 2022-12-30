import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


class Board:
    """ a square board """

    def __init__(self, board):
        self.board = board
        # assume square board
        self.size = len(board[0])
        self.marks = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.won = False
        self.score = None

    def __position(self, n):
        """ return, if found, the coordinates
        of the number n in the bingo board"""
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[i][j] == n:
                    return i, j
        return None

    def check_win(self):
        """ check whether the board is won, given its marks
        (full row or column of 1s)"""
        check_rows = any(all(row) for row in self.marks)
        check_cols = any(all(col) for col in list(zip(*self.marks)))
        self.won = check_rows or check_cols
        return self.won

    def __sum_unmarked(self):
        """ compute the sum of all unmarked number
        of a board"""
        res = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if not self.marks[i][j]:
                    res += self.board[i][j]
        return res

    def calc_score(self, n):
        self.score = n * self.__sum_unmarked()
        return self.score

    def mark_n(self, n):
        pos = self.__position(n)
        if pos is not None:
            self.marks[pos[0]][pos[1]] = 1
            # check if win
            if self.check_win():
                self.calc_score(n)


@aoc.pretty_solution(1)
def part1(numbers, raw_boards):
    """ brute force until a board wins, number by number"""
    boards = [Board(b) for b in raw_boards]

    for n in numbers:
        # mark n in every board (if found)
        for b in boards:
            b.mark_n(n)
            if b.won:
                return b.score
    return None


@aoc.pretty_solution(2)
def part2(numbers, raw_boards):
    # init a corresponding table of marked numbers for each board
    boards = [Board(b) for b in raw_boards]

    last_win_score = 0
    for n in numbers:
        # mark n in every board (if found)
        for b in boards:
            # check only if not already won
            if not b.won:
                b.mark_n(n)
                if b.won:
                    last_win_score = b.score
    return last_win_score


def main():
    raw = aoc_parse.input_as_lines(prj_path + '/year2021/input/day04.txt')
    # get drawn numbers in order
    numbers = [int(x) for x in raw[0].split(',')]
    # get bingo boards as (list of) lists of lists
    BOARD_SZ = 5
    boards = []
    for i in range(2, len(raw), BOARD_SZ + 1):
        boards.append([[int(x) for x in raw[j].split()] for j in range(i, i + BOARD_SZ)])
    return part1(numbers, boards), part2(numbers, boards)


if __name__ == "__main__":
    main()
