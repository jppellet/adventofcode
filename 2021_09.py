from itertools import product
from math import prod
from utils import *

SAMPLE = False
data = read_lines(input_for(__file__, SAMPLE), lambda line: list(map(int, list(line))))
width, height = len(data[0]), len(data)

def neighborhood(x: int, y: int) -> list[tuple[int, int]]:
    xs = range(max(x - 1, 0), min(x + 2, height))
    ys = range(max(y - 1, 0), min(y + 2, width))
    return [(_x, _y) for _x in xs for _y in ys if (_x, _y) != (x, y) and (x == _x or y == _y)]

# Part 1

lows: list[tuple[int, int]] = []
for x, y in product(range(height), range(width)):
    if all(data[_x][_y] > data[x][y] for _x, _y in neighborhood(x, y)):
        lows.append((x, y))

risk = lambda coord: data[coord[0]][coord[1]] + 1
print(sum(map(risk, lows)))

# Part 2

basins = [[-1 for _ in range(width)] for _ in range(height)]

for i, (x, y) in enumerate(lows):
    def look_around(x: int, y: int) -> None:
        basins[x][y] = i
        for _x, _y in neighborhood(x, y):
            if basins[_x][_y] == -1 and data[_x][_y] != 9:
                look_around(_x, _y)
    look_around(x, y)

basins_flat = flatten(basins)
basin_sizes = list(map(lambda i: basins_flat.count(i), range(len(lows))))
print(prod(sorted(basin_sizes, reverse=True)[:3]))