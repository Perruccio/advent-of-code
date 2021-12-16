import sys
from solutions import *
from collections import OrderedDict

answers = OrderedDict({
    'day01' : (1709, 1761),
    'day02' : (2117664, 2073416724),
    'day03' : (2972336, 3368358),
    'day04' : (49860, 24628),
    'day05' : (4421, 18674),
    'day06' : (388739, 1741362314973),
    'day07' : (331067, 92881128),
    'day08' : (488, 1040429),
    'day09' : (532, 1110780),
    'day10' : (411471, 3122628974),
    'day11' : (1659, 227),
    'day12' : (5104, 149220),
    'day13' : (788, 102),
    'day14' : (2975, 3015383850689),
    'day15' : (562, 2874),
    'day16' : (854, 186189840660),
})

def print_test(day):
    if len(day) == 4:
        day = day[:3] + '0' + day[-1]
    p1, p2 = globals()[day].main(pretty_print=False)
    res1 = "OK" if p1 == answers[day][0] else "ERROR"
    res2 = "OK" if p2 == answers[day][1] else "ERROR"
    print('Day ' + day.replace('day', '') + f':\tpart 1 {res1}, part 2 {res2}')

def main():
    if not (len(sys.argv) == 1 or len(sys.argv) == 2):
        print('Usage: py test.py [day1]')

    if len(sys.argv) == 1:
        for test in answers:
            print_test(test)
    else:
        print_test(sys.argv[1])

if __name__ == "__main__":
    main()