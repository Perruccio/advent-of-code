from collections import OrderedDict

from advent_of_code.year2021.solutions import *  # noqa

answers = OrderedDict({
    'day01': (1709, 1761),
    'day02': (2117664, 2073416724),
    'day03': (2972336, 3368358),
    'day04': (49860, 24628),
    'day05': (4421, 18674),
    'day06': (388739, 1741362314973),
    'day07': (331067, 92881128),
    'day08': (488, 1040429),
    'day09': (532, 1110780),
    'day10': (411471, 3122628974),
    'day11': (1659, 227),
    'day12': (5104, 149220),
    'day13': (788, 102),
    'day14': (2975, 3015383850689),
    'day15': (562, 2874),
    'day16': (854, 186189840660),
    'day17': (8911, 4748),
    'day18': (4391, 4626),
    'day19': (306, 9764),
    'day20': (4928, 16605),
    'day21': (752745, 309196008717909),
    'day22': (580098, 1134725012490723),
    'day23': (15412, 52358),
    'day24': (91599994399395, 71111591176151),
    'day25': (295, None),
})


def test():
    for day in answers:
        p1, p2 = globals()[day].main(pretty_print=False)
        assert p1, p2 == answers[day]
        res1 = "OK" if p1 == answers[day][0] else "ERROR"
        res2 = "OK" if p2 == answers[day][1] else "ERROR"
        print('Day ' + day.replace('day', '') + f':\tpart 1 {res1}, part 2 {res2}')


if __name__ == "__main__":
    test()
