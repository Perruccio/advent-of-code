import re

RE = {"int": r"[+-]?\d+"}


def get_ints(line):
    return list(map(int, re.findall(RE["int"], line)))


def as_lines(raw: str) -> list[str]:
    """Return a list where each line in the input file is an element of the list"""
    return raw.split("\n")


def map_by_line(raw: str, func) -> list:
    """Returns the content of the input file as a list of mapped lines"""
    return list(map(func, as_lines(raw)))


def input_as_list_of_lists(raw: str, delim: str = "", func=int) -> list[list]:
    """Parse input where data are lists separated by a delimiter line"""
    return list(
        map(
            lambda line: [func(x) for x in line.split("\n")],
            raw.split("\n" + delim + "\n"),
        )
    )


# deprecated functions
def input_as_string(filename):
    with open(filename) as f:
        return f.read().rstrip("\n")
    
def input_as_lines(filename: str) -> list[str]:
    """Return a list where each line in the input file is an element of the list"""
    return input_as_string(filename).split("\n")


def map_input_lines(filename: str, func) -> list:
    """Returns the content of the input file as a list of mapped lines"""
    return list(map(func, input_as_lines(filename)))
