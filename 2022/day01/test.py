import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
parent_dir = curr_dir.parent
sys.path.append(str(parent_dir))
from day01 import solution

from utils.test import check_values


def check():
    check_values(int(str(curr_dir)[-2:]), solution.main(), (72240, 210957))


if __name__ == "__main__":
    check()
