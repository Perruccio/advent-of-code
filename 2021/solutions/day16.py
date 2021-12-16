import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

class Packet:
    def __init__(self, version, type, literal=None, sub_packets=None):
        self.version = version
        self.type = type
        self.literal = literal
        self.sub_packets = [] if sub_packets is None else sub_packets

    def sum_versions(self):
        return self.version + sum([p.sum_versions for p in self.sub_packets])

def hex2bin(hex_digits):
    return "".join([bin(int(hex_digit, 16))[2:].zfill(4) for hex_digit in hex_digits])

def get_literal(b, i):
    literal = ""
    while b[i] == '1':
        literal, i = literal + b[i+1:i+5], i+5
    literal, i = literal + b[i+1:i+5], i+5
    while i < len(b) and b[i] == '0':
        i += 1
    return int(literal, 2), i

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
        sub_packets = []
        length_type, i = b[i], i+1 
        if length_type == 0:
            end = i+15
            while i < end:
                sub_packet, i = get_packet(b, i)
                sub_packets.append(sub_packet)
        else:
            n_sub_packets, i = int(b[i:i+11]), i+11
            for _ in range(n_sub_packets):
                sub_packet, i = get_packet(b, i)
                sub_packets.append(sub_packet)
        return Packet(version, type, sub_packets=sub_packets), i

def part1(data):
    b = hex2bin(data)
    i = 0
    tot_versions = 0
    while i < len(b):
        packet, i = get_packet(b, i)
        tot_versions += packet.sum_versions()
    return tot_versions

def part2(data):
    pass

def main(pretty_print = True):
    
    data = input_as_string(prj_path + '/input/day16test.txt')

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)
   
if __name__ == "__main__":
    main()