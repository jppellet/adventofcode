from utils import *
from itertools import count


SAMPLE = False
data = read_lines(input_for(__file__, SAMPLE), lambda l: list(map(int, l)))
height, width = len(data), len(data[0])

def print_data() -> None:
    for i in range(len(data)):
        print(join(data[i], ""))
    print()

def neighborhood(x: int, y: int) -> list[tuple[int, int]]:
    xs = range(max(x - 1, 0), min(x + 2, height))
    ys = range(max(y - 1, 0), min(y + 2, width))
    return [(_x, _y) for _x in xs for _y in ys if (_x, _y) != (x, y)]

total_flashes = 0

def do_step() -> None:
    global total_flashes

    flashed = [[False for _ in range(width)] for _ in range(height)]

    for x in range(height):
        for y in range(width):
            data[x][y] += 1

    def flash(x: int, y: int) -> None:
        data[x][y] = 0
        flashed[x][y] = True
        for _x, _y in neighborhood(x, y):
            if not flashed[_x][_y]:
                data[_x][_y] += 1
        for _x, _y in neighborhood(x, y):
            if data[_x][_y] > 9 and not flashed[_x][_y]:
                flash(_x, _y)

    for x in range(height):
        for y in range(width):
            if data[x][y] > 9:
                flash(x,y)

    for x in range(height):
        for y in range(width):
            if flashed[x][y]:
                total_flashes += 1
                data[x][y] = 0


for step in count(1):
    do_step()
    if step == 100:
        print(total_flashes)

    if all(map(lambda row: all(map(lambda cell: cell == 0, row)), data)):
        break

print(step)