from typing import List
import re

RE = {"int": r"[+-]?\d+"}


def get_ints(line):
    return list(map(int, re.findall(RE["int"], line)))


def input_as_string(filename: str) -> str:
    """Returns the content of the input file as a string"""
    with open(filename) as f:
        return f.read().rstrip("\n")


def input_as_lines(filename: str) -> List[str]:
    """Return a list where each line in the input file is an element of the list"""
    return input_as_string(filename).split("\n")


def map_input_lines(filename: str, func) -> List:
    """Returns the content of the input file as a list of mapped lines"""
    return list(map(func, input_as_lines(filename)))


def input_as_list_of_lists(filename: str, delim: str = "", func=int) -> List[List]:
    """Parse input where data are lists separated by a delimiter line"""
    return list(
        map(
            lambda line: [func(x) for x in line.split("\n")],
            input_as_string(filename).split("\n" + delim + "\n"),
        )
    )
