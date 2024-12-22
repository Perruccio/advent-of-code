from advent_of_code.lib.all import *

def get_input(file):
    raw = aoc.read_input(2024, 21, file)
    return aoc_parse.as_lines(raw)


class Keypad(ABC):

    @classmethod
    def convert_move(cls, move):
        match move:
            case  1 : return "v"
            case -1 : return "^"
            case  1j: return ">"
            case -1j: return "<"
        raise

    @classmethod
    def convert_sequence(cls, seq):
        return ''.join(list(map(cls.convert_move, seq)))


    def get_all(self, keys):
        keys = list(map(self.convert_key, keys))
        starts = [self.p] + keys[:-1]
        ends = keys
        res = [""]
        for start, end in zip(starts, ends):
            new_seqs = self.get_moves(start, end)
            new_seqs = list(map(lambda seq: self.convert_sequence(seq) + "A", new_seqs))
            res = [seq1 + seq2 for seq1 in res for seq2 in new_seqs]
        return res

    def get_moves(self, start, end):
        delta = end - start
        moves = [aoc_math.sign(delta.real)] * abs(int(delta.real))
        moves += [aoc_math.sign(delta.imag)*1j] * abs(int(delta.imag))
        res = []
        for perm in set(permutations(moves)):
            p = start
            for move in perm:
                p += move
                if p == self.avoid:
                    break
            else:
                res.append(perm)
        return res
  

class NumericalKeypad(Keypad):
    def __init__(self):
        self.p = 3 + 2j
        self.avoid = 3

    def convert_key(self, digit):
        # convert digit to position in grid
        if digit in "789":
            return (int(digit) - 7)*1j
        if digit in "456":
            return 1 + (int(digit) - 4)*1j
        if digit in "123":
            return 2 + (int(digit) - 1)*1j
        if digit == "0":
            return 3 + 1j
        if digit == "A":
            return 3 + 2j
        raise


class DirectionalKeyboard(Keypad):
    def __init__(self):
        self.p = 0 + 2j
        self.avoid = 0

    def convert_key(self, key):
        match key:
            case "^" : return 1j
            case "<" : return 1
            case "v" : return 1 + 1j
            case ">" : return 1 + 2j
            case "A" : return 2j
        raise

def score(code, moves):
    print(f"{len(moves)} * {int(code[:-1])}")
    return int(code[:-1]) * len(moves)

@aoc.pretty_solution(1)
def part1(codes):
    score = 0
    for code in codes:
        nk = NumericalKeypad()
        dk1, dk2, dk3 = [DirectionalKeyboard() for _ in range(3)]
        res = []
        for s1 in nk.get_all(code):
            res += dk1.get_all(s1)
        res2 = []
        for s2 in res:
            res2 += dk2.get_all(s2)
        res3 = []
        for s3 in res2:
            res3 += dk3.get_all(s3)
        score += min(map(len, res3))*int(code[:-1])
        print(f"{min(map(len, res3))}*{int(code[:-1])}")
    return score
    

@aoc.pretty_solution(2)
def part2(data):
    return

def unit_test():
    nk = NumericalKeypad()
    assert nk.get_moves("029A") == "<A^A^^>AvvvA"
    print("Unit tests OK")

def test():
    data = get_input("input.txt")
    part1(deepcopy(data))
    part2(data)
    # assert part1(deepcopy(data)) == 217662
    # assert part2(data) == 
    print("Test OK")


if __name__ == "__main__":
    test()
