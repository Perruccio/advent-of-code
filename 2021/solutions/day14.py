import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
from collections import Counter

def insert(polymer, rules):
    inserted, occurrences = Counter(), Counter()
    for pair, x in polymer.items():
        a = rules[pair]
        inserted[pair[0] + a] += x
        inserted[a + pair[1]] += x
        occurrences[a] += x
    return inserted, occurrences

def solve(polymer, rules, n):
    # model the data as pairs, don't mind the whole sequence
    # every pair is independent
    pairs = Counter({pair: polymer.count(pair) for pair in rules})
        
    # keep count of occurences of each letter
    occurrences = Counter(polymer)
    for _ in range(n): 
        pairs, occ = insert(pairs, rules)
        occurrences += occ
    return max(occurrences.values()) - min(occurrences.values())

def part1(polymer, rules):
    return solve(polymer, rules, 10)

def part2(polymer, rules):
    return solve(polymer, rules, 40)

def main(pretty_print = True):
    data = input_as_lines(prj_path + '/input/day14.txt')
    
    polymer = data[0]
    rules = dict(rule.split(' -> ') for rule in data[2:])

    if (pretty_print):
        print_results(1, part1, polymer, rules)
        print_results(2, part2, polymer, rules)
    else:
        return part1(polymer, rules), part2(polymer, rules)
   
if __name__ == "__main__":
    main()