from typing import Tuple
from utils import *

SAMPLE = False
data = read_first_line(input_for(__file__, SAMPLE), ",", int)

def fuel_linear(pos: Tuple[int, int]) -> int:
    return abs(pos[1] - pos[0])

def fuel_quadratic(pos: Tuple[int, int]) -> int:
    d = abs(pos[1] - pos[0])
    return (d * (d + 1)) // 2

n, check_range = len(data), range(min(data), max(data) + 1)

for fuel in fuel_linear, fuel_quadratic:
    spent_fuel = map(lambda i: sum(map(fuel, zip(data, [i] * n))), check_range)
    print(min(spent_fuel))