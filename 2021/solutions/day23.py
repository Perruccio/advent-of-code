import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
from collections import deque
import copy

def target_room(type, diagram):
    room = set()
    for i in range(len(diagram)):
        for j in range(len(diagram[0])):
            if diagram[i][j] == type:
                room.add((i, j))
    return room

TARGET1 = [
'#############',
'#...........#',
'###A#B#C#D###',
'  #A#B#C#D#  ',
'  #########  '
]

TARGET2 = [
'#############',
'#...........#',
'###A#B#C#D###',
'  #A#B#C#D#  ',
'  #A#B#C#D#  ',
'  #A#B#C#D#  ',
'  #########  '
]

TARGET1 = [list(line) for line in TARGET1]
TARGET2 = [list(line) for line in TARGET2]
TARGET_ROOMS1 = {t:target_room(t, TARGET1) for t in 'ABCD'}
TARGET_ROOMS2 = {t:target_room(t, TARGET2) for t in 'ABCD'}
TARGET_COLS = {t: 3 + 2 * (ord(t) - ord('A')) for t in 'ABCD'}

ENERGY = {t: 10**(ord(t) - ord('A')) for t in 'ABCD'}

def empty(pos, diagram):
    return diagram[pos[0]][pos[1]] == '.'

def wall(pos, diagram):
    return diagram[pos[0]][pos[1]] == '#' or diagram[pos[0]][pos[1]] == ' '

def door(pos, diagram):
    i, j = pos
    return wall((i-1, j), diagram) and not wall((i+1, j), diagram)

def hallway(pos, diagram=TARGET1):
    return pos[0] == 1 and 1 <= pos[1] < len(diagram[0]) - 1

def in_target(pos, type, target_rooms, diagram):
    for ii, jj in target_rooms[type]:
        if not empty((ii, jj), diagram) and diagram[ii][jj] != type:
            return False
    return pos in target_rooms[type]

def room(pos, diagram):
    return wall((pos[0], pos[1] - 1), diagram) and wall((pos[0], pos[1] + 1), diagram)

def view_diagram(diagram):
    return ["".join(l) for l in diagram]

def string_diagram(diagram):
    return "".join(["".join(l) for l in diagram])

def move_hallway(i, j, dir, diagram, e, delta_e):
    ms = set()
    while empty((i, j+dir), diagram):
        j += dir
        e += delta_e
        # don't stop outside rooms
        if wall((i+1, j), diagram):
            ms.add(((i, j), e))
    return ms

class Amph():
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.in_target = False

    def moves(self, diagram, target_rooms):
        if self.in_target:
            return set()
        i, j = self.pos
        e = 0
        delta_e = ENERGY[self.type]
        if room(self.pos, diagram):
            # go up until hallway then go left and right
            while empty((i-1, j), diagram):
                i -= 1
                e += delta_e
            # hallway
            if i != 1:
                return set()
            # right
            ms = move_hallway(i, j, 1, diagram, e, delta_e)
            # left
            ms.update(move_hallway(i, j, -1, diagram, e, delta_e))
            return ms
        else:
            for ii, jj in target_rooms[self.type]:
                if not empty((ii, jj), diagram) and diagram[ii][jj] != self.type:
                    return set()
            # can only go to target
            # go left xor right then down
            tc = TARGET_COLS[self.type]
            dir = sign(tc - self.pos[1])
            # follow dir until door of target room
            while empty((i, j + dir), diagram):
                j += dir
                e += delta_e
                if j == tc:
                    break
            # check right column
            if j != tc:
                return set()
            # got down until empty
            while empty((i+1, j), diagram):
                i += 1
                e += delta_e
            return set([((i, j), e)])

def solve(diagram, target_diagram, target_rooms):
    w, h = len(diagram), len(diagram[0])

    # init amphs
    amphs = []
    frontier = []
    for i in range(w):
        for j in range(h):
            if not wall((i, j), diagram) and not empty((i, j), diagram):
                amph = Amph((i, j), diagram[i][j])
                amphs.append(amph)
    
    min_e = float('inf')
    frontier = deque([(diagram, amphs, 0)])
    visited = {}
    while frontier:
        diagram, amphs, e = frontier.pop()

        if e >= min_e:
            continue
        elif diagram == target_diagram:
            min_e = e
            continue
        # skip if already visited with higher energy
        s = string_diagram(diagram) 
        if s in visited and e >= visited[s]:
            continue
        visited[s] = e

        # dfs
        new_frontier = list()
        in_t = False
        for i, amph in enumerate(amphs):
            if in_t:
                break
            moves = amph.moves(diagram, target_rooms)
            for new_pos, delta_e in moves:
                # new diagram
                new_diagram = copy.deepcopy(diagram)
                new_diagram[amph.pos[0]][amph.pos[1]] = '.'
                new_diagram[new_pos[0]][new_pos[1]] = amph.type
                # move amph
                new_amph = copy.copy(amph)
                new_amph.pos = new_pos
                new_amphs = copy.copy(amphs)
                new_amphs[i] = new_amph
                # if in target, this move is correct and avoid check other (equivalent) possibilities
                if in_target(new_pos, amph.type, target_rooms, new_diagram):
                    in_t = True
                    new_amphs[i].in_target = True
                    new_frontier = [(new_diagram, new_amphs, e + delta_e)]
                    break
                else:
                    # add new state
                    new_frontier.append((new_diagram, new_amphs, e + delta_e))
        frontier += new_frontier
    return min_e

def part1(data):
    return solve(data, TARGET1, TARGET_ROOMS1)

def part2(data):
    l1 = '  #D#C#B#A#  '
    l2 = '  #D#B#A#C#  '
    data = data[:3] + [list(l1)] + [list(l2)] + data[3:]
    return solve(data, TARGET2, TARGET_ROOMS2)

def main(pretty_print = True):
    def map_line(line):
        return list(line)

    data = map_input_lines(prj_path + '/2021/input/day23.txt', map_line)
    data[-2] += [' '] * 2
    data[-1] += [' '] * 2

    if (pretty_print):
        output_procedure(1, part1, True, data)
        output_procedure(2, part2, True, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()