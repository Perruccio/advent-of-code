import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
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

def empty(pos, diagram):
    return diagram[pos[0]][pos[1]] == '.'

def wall(pos, diagram):
    return diagram[pos[0]][pos[1]] == '#' or diagram[pos[0]][pos[1]] == ' '

def door(pos, diagram):
    i, j = pos
    return wall((i-1, j), diagram) and not wall((i+1, j), diagram)

def hallway(pos, diagram=TARGET1):
    return pos[0] == 1 and 1 <= pos[1] < len(diagram[0]) - 1

def in_target(pos, type, diagram, target_rooms):
    return pos in target_rooms[type] and (wall((pos[0]+1, pos[1]), diagram) or diagram[pos[0]+1][pos[1]] == type)

def room(pos, diagram):
    return wall((pos[0], pos[1] - 1), diagram) and wall((pos[0], pos[1] + 1), diagram)

def view_diagram(diagram):
    return ["".join(l) for l in diagram]

def string_diagram(diagram):
    return "".join(["".join(l) for l in diagram])

class Amph():
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.energy = 10**(ord(type) - ord('A'))

    def moves(self, diagram, target_rooms):
        if in_target(self.pos, self.type, diagram, target_rooms):
            return set()
        ms = set()
        visited = set()
        in_room = room(self.pos, diagram)
        frontier = set([(self.pos, 0)])
        while frontier:
            p, e = frontier.pop()
            visited.add(p)
            for m in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_pos = p[0] + m[0], p[1] + m[1]
                new_e = e + self.energy
                check = empty(new_pos, diagram)
                if check and in_target(new_pos, self.type, diagram, target_rooms):
                    return set([(new_pos, new_e)])
                check = check and new_pos not in visited
                check = check and (in_room and hallway(new_pos, diagram) or m[0] == -1 or not in_room)
                if check:
                    frontier.add((new_pos, new_e))
                    if new_pos != self.pos and not door(new_pos, diagram) and in_room:
                        ms.add((new_pos, new_e))
        return ms

def part1(diagram0):
    w, h = len(diagram0), len(diagram0[0])

    # init amphs
    amphs = []
    frontier = []
    for i in range(w):
        for j in range(h):
            if not wall((i, j), diagram0) and not empty((i, j), diagram0):
                amph = Amph((i, j), diagram0[i][j])
                amphs.append(amph)
    
    min_e = float('inf')
    frontier = deque([(diagram0, amphs, 0)])
    visited = {}
    while frontier:
        diagram, amphs, e = frontier.pop()

        if e >= min_e:
            continue
        elif diagram == TARGET1:
            min_e = e
            continue

        # skip if already visited with higher energy
        s = string_diagram(diagram) 
        if s in visited and e >= visited[s]:
            continue
        visited[s] = e

        new_frontier = deque()
        in_t = False
        for i, amph in enumerate(amphs):
            if in_t:
                break
            moves = amph.moves(diagram, TARGET_ROOMS1)
            for new_pos, delta_e in moves:
                new_diagram = copy.deepcopy(diagram)
                new_diagram[amph.pos[0]][amph.pos[1]] = '.'
                new_diagram[new_pos[0]][new_pos[1]] = amph.type
                new_amph = copy.deepcopy(amph)
                new_amph.pos = new_pos
                new_amphs = amphs[:]
                new_amphs[i] = new_amph
                new_frontier.append((new_diagram, new_amphs, e + delta_e))
                if in_target(new_pos, amph.type, diagram, TARGET_ROOMS1):
                    in_t = True
                    new_frontier = deque([(new_diagram, new_amphs, e + delta_e)])
                    break
        frontier.extend(new_frontier)
    return min_e

def part2(data):
    pass
def main(pretty_print = True):
    def map_line(line):
        return list(line)

    data = map_input_lines(prj_path + '/input/day23.txt', map_line)
    data[-2] += [' '] * 2
    data[-1] += [' '] * 2

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()