from utils import *
from sys import argv, exit
from dataclasses import dataclass

SAMPLE = len(argv) < 2 or argv[1] != "real"

@dataclass
class Cell:
    risk: int
    risk_path: int = -1
    prev: Optional['Cell'] = None
    on_final_path: bool = False

def make_cell(c: str) -> Cell:
    return Cell(int(c))

def inc_cell(cell: Cell) -> Cell:
    risk1 = cell.risk + 1
    return Cell(1 if risk1 == 10 else risk1, -1)    

def neighborhood(x: int, y: int) -> list[tuple[int, int]]:
    xs = range(max(x - 1, 0), min(x + 2, height))
    ys = range(max(y - 1, 0), min(y + 2, width))
    return [(_x, _y) for _x in xs for _y in ys if (_x, _y) != (x, y) and (x == _x or y == _y)]

def augment_map() -> None:
    for row in data:
        vals = row[:]
        for _ in range(4):
            vals = list(map(inc_cell, vals))
            row.extend(vals)
    valss = data[:]
    for _ in range(4):
        valss = list(map(lambda row: list(map(inc_cell, row)), valss))
        data.extend(valss)


data = read_lines(input_for(__file__, SAMPLE), lambda line: list(map(make_cell, line)))
augment_map()

data[0][0].risk_path = 0
width, height = len(data[0]), len(data)

def print_data(detailed: bool) -> None:
    to_str = (lambda cell: cell.risk) if not detailed else \
        (lambda cell: f"{cell.risk} {cell.risk_path:3}     ")
    for row in data:
        print(join(map(to_str, row), ""))

visit_queue: list[tuple[int, int]] = [(0, 0)]
while len(visit_queue) != 0:
    # print(len(visit_queue))
    x, y = visit_queue.pop(0)
    cell = data[x][y]
    for _x, _y in neighborhood(x, y):
        neighbor = data[_x][_y]
        new_risk_path = cell.risk_path + neighbor.risk
        if neighbor.risk_path == -1 or new_risk_path < neighbor.risk_path:
            neighbor.risk_path = new_risk_path
            neighbor.prev = cell
            visit_queue.append((_x, _y))

# print_data(detailed=True)
print(data[height // 5 -1][width // 5 -1].risk_path)
print(data[-1][-1].risk_path)

# rest is optional, only for visualization

# back track
path_cell = data[-1][-1]
while True:
    path_cell.on_final_path = True
    if path_cell.prev is None:
        break
    path_cell = path_cell.prev

with open("2021_15_out.txt", "w") as file:
    for row in data:
        file.write(join(map(lambda cell: "W" if cell.on_final_path else " ", row), "") + "\n")