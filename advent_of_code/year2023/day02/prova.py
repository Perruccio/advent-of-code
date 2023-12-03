from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
import re

line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"

v = set(re.findall(fr"{aoc_parse.RE['int']} (\w+)", line))
print(v)
