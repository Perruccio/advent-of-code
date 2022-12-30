from pathlib import Path, PurePath
import time


def read_input(year, day, file_name):
    """Returns the content of the input file as a string"""
    with open(Path.cwd() / PurePath(f"advent_of_code/year{year}/day{day:02}/{file_name}")) as f:
        return f.read().rstrip("\n")


def pretty_solution(part):
    def decorator(func):
        def wrapper(*arg, **kw):
            t = time.time_ns()
            ans = func(*arg, **kw)
            ns = time.time_ns() - t  # nanoseconds
            if isinstance(ans, list):
                print(f"Part {part}: \t({time_measure(ns)})")
                for line in ans:
                    print(line)
            else:
                print(f"Part {part}: {ans} \t({time_measure(ns)})")
            return ans

        return wrapper

    return decorator


def time_measure(ns):
    # compute appropriate time measure units. Input is time in nanoseconds
    i = 0
    while ns >= 1000 and i < 3:
        ns /= 1000
        i += 1
    return str(f"{ns:.2f}") + " " + ["ns", "us", "ms", "s"][i]
