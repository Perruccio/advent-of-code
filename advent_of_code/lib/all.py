from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc, math as aoc_math
from advent_of_code.lib.std import *
from collections import deque, defaultdict
from copy import deepcopy, copy
import re
from functools import lru_cache, cmp_to_key, cache
from operator import add, mul
from math import log10, prod
from itertools import zip_longest, permutations, combinations, product as cart_prod
from abc import ABC
from heapq import heappop, heappush