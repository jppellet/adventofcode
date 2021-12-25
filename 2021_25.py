from sys import argv, exit
from utils import *

SAMPLE = len(argv) < 2 or argv[1] != "real"
grid = read_lines(input_for(__file__, SAMPLE), lambda line: list(line))
height = len(grid)
width = len(grid[0])

def print_data() -> None:
    for line in grid:
        print("".join(line))
    print("\n")


def step() -> bool:
    global grid
    changed = False

    new_grid = [["." for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == ">":
                nextx = (x + 1) % width
                if grid[y][nextx] == ".":
                    new_grid[y][nextx] = ">"
                    changed = True
                else:
                    new_grid[y][x] = ">"
            elif grid[y][x] == "v":
                new_grid[y][x] = "v"

    grid = new_grid
    new_grid = [["." for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "v":
                nexty = (y + 1) % height
                if grid[nexty][x] == ".":
                    new_grid[nexty][x] = "v"
                    changed = True
                else:
                    new_grid[y][x] = "v"
            elif grid[y][x] == ">":
                new_grid[y][x] = ">"

    grid = new_grid
    return changed

print_data()

c = 0
while True:
    changed = step()
    c += 1
    if not changed:
        print_data()
        print_result(f"After {c} steps")
        break
    