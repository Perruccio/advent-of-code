import time


def print_result(part, func, *arg, **kw):
    t = time.time_ns()
    ans = func(*arg, **kw)
    ns = time.time_ns() - t  # nanoseconds
    print(f"Part {part}: {ans} \t({time_measure(ns)})")
    return ans


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
    # compute appropriate time measure units
    i = 0
    while ns >= 1000 and i < 3:
        ns /= 1000
        i += 1
    return str(f"{ns:.2f}") + " " + ["ns", "us", "ms", "s"][i]


def print_image(image):
    for line in image:
        for c in line:
            if c:
                print("* ", end="")
            else:
                print("  ", end="")
        print()
