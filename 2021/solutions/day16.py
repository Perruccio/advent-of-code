import sys
import pathlib
from typing import Literal
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
from math import prod

class Packet:
    def __init__(self, version, type, literal=None, sub_packets=None):
        self.version = version
        self.type = type
        self.literal = literal
        self.sub_packets = [] if sub_packets is None else sub_packets

    def sum_versions(self):
        return self.version + sum([p.sum_versions() for p in self.sub_packets])

    def evaluate(self):
        match self.type:
            case 0:
                return sum([p.evaluate() for p in self.sub_packets])
            case 1:
                return prod([p.evaluate() for p in self.sub_packets])
            case 2:
                return min([p.evaluate() for p in self.sub_packets])
            case 3:
                return max([p.evaluate() for p in self.sub_packets])
            case 4:
                return self.literal
            case 5:
                return self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate()
            case 6:
                return self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate()
            case 7:
                return self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate()

def get_literal(b, i):
    # return value of the literal and advance index
    literal = ""
    while b[i] == '1':
        literal, i = literal + b[i+1:i+5], i+5
    literal, i = literal + b[i+1:i+5], i+5
    return int(literal, 2), i

def get_sub_packets(b, i):
    sub_packets = []
    length_type, i = b[i], i+1
    if length_type == '0':
        b_length, i = int(b[i:i+15], 2), i+15
        end = i + b_length
        while i < end:
            sub_packet, i = get_packet(b, i)
            sub_packets.append(sub_packet)
    else:
        n_sub_packets, i = int(b[i:i+11], 2), i+11
        for _ in range(n_sub_packets):
            sub_packet, i = get_packet(b, i)
            sub_packets.append(sub_packet)
    return sub_packets, i

def get_packet(b, i):
    # version
    version, i = int(b[i:i+3], 2), i+3
    # type id
    type, i = int(b[i:i+3], 2), i+3
    # data
    if type == 4:
        # literal
        literal, i = get_literal(b, i)
        return Packet(version, type, literal=literal), i
    else:
        # is operator
        sub_packets, i = get_sub_packets(b, i)
        return Packet(version, type, sub_packets=sub_packets), i

def decode(data):
    b = hex2bin(data)
    i = 0
    while i < len(b):
        packet, i = get_packet(b, i)
        while i < len(b) and b[i] == '0':
            i += 1
        yield packet

def part1(data):
    return sum([p.sum_versions() for p in decode(data)])

def part2(data):
    return next(decode(data)).evaluate()

def main(pretty_print = True):
    
    data = input_as_string(prj_path + '/input/day16.txt')

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)
   
if __name__ == "__main__":
    main()