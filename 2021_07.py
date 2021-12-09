from utils import *
from itertools import starmap

SAMPLE = False
data = read_first_line(input_for(__file__, SAMPLE), ",", int)

def fuel_linear(x: int, y: int) -> int:
    return abs(x - y)

def fuel_quadratic(x: int, y: int) -> int:
    d = abs(x - y)
    return (d * (d + 1)) // 2

n, check_range = len(data), range(min(data), max(data) + 1)

for fuel in fuel_linear, fuel_quadratic:
    spent_fuel = map(lambda i: sum(starmap(fuel, zip(data, [i] * n))), check_range)
    print(min(spent_fuel))