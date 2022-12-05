import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils.aoc import *
import copy


class CraneStep:
    def __init__(self, n, frm, to):
        self.n = n
        self.frm = frm - 1
        self.to = to - 1


def get_input():
    # read from file as list of strings
    lines = input_as_lines(str(curr_dir) + "/input.txt")

    ## first parse crates
    # stop at first empty line
    idx = lines.index("")
    # transpose lines in columns
    raw = zip(*lines[:idx])
    # identify actual columns with crates (second to last char is a letter)
    # ignore last element (stack id), ignore empty space and reverse order
    crates = [list("".join(line[-2::-1]).strip()) for line in raw if line[-2].isalpha()]

    ## parse instruction steps
    def get_step(line):
        # split line at whitespace, take 1,3,5 elements and map to int
        return CraneStep(*list(map(int, line.split()[1::2])))

    steps = list(map(get_step, lines[idx + 1 :]))
    return crates, steps


def do_step(crates, step: CraneStep, multiple):
    # lift last n crates of stack frm
    lift_crate = crates[step.frm][-step.n :]
    # delete them
    del crates[step.frm][-step.n :]
    # add to new stack, in reversed order if needed
    crates[step.to].extend(lift_crate if multiple else lift_crate[::-1])
    return crates


def part1(crates, steps):
    crates = copy.deepcopy(crates)
    for step in steps:
        do_step(crates, step, False)
    return "".join([crate[-1] for crate in crates])


def part2(crates, steps):
    crates = copy.deepcopy(crates)
    for step in steps:
        do_step(crates, step, True)
    return "".join([crate[-1] for crate in crates])


def main():
    crates, steps = get_input()
    return print_results(1, part1, crates, steps), print_results(2, part2, crates, steps)


def test():
    """test for pytest"""
    assert main() == ("WSFTMRHPP", "GSLCMFBRP")


if __name__ == "__main__":
    test()
