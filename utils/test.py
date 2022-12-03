def check_values(day, reference_values, test_values):
    res1 = "OK" if reference_values[0] == test_values[0] else "ERROR"
    res2 = "OK" if reference_values[1] == test_values[1] else "ERROR"
    print(f"Day {day}:\tpart 1 {res1}, part 2 {res2}")
