import solution


def test():
    p1, p2 = solution.main()
    res1 = "OK" if p1 == 8890 else "ERROR"
    res2 = "OK" if p2 == 10238 else "ERROR"
    print(f"Day 1:\tpart 1 {res1}, part 2 {res2}")


if __name__ == "__main__":
    test()
