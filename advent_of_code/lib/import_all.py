# ruff: noqa: F401
from collections import deque, defaultdict
from copy import deepcopy
from advent_of_code.lib import aoc
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib.geometry import Cuboid
from advent_of_code.lib.math import *
from math import prod, lcm
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Dict, List