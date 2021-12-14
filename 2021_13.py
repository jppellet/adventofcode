from utils import *

SAMPLE = False

data = read_lines(input_for(__file__, SAMPLE), str)
sep_line = data.index("")


def parse_coords(line: str) -> tuple[int, int]:
    parts = line.split(",")
    return int(parts[0]), int(parts[1])


def parse_fold(line: str) -> tuple[str, int]:
    parts = line.split("=")
    axis = parts[0].split(" ")[-1]
    return axis, int(parts[1])


dots = list(map(parse_coords, data[:sep_line]))
folds = list(map(parse_fold, data[sep_line + 1 :]))

width = max(x for x, y in dots) + 1
height = max(y for x, y in dots) + 1

sheet = [[False for _ in range(width)] for _ in range(height)]

for x, y in dots:
    sheet[y][x] = True

def print_sheet() -> None:
    for line in sheet:
        print(join(line, "", lambda b: "\033[7m \033[0m" if b else " "))


for i, (axis, pos) in enumerate(folds):
    before = range(pos - 1, -1, -1)  # lines/rows before fold
    if axis == "y":
        after = range(pos + 1, len(sheet))  # rows after fold
        for u, d in zip(before, after):
            for x in range(len(sheet[0])):
                sheet[u][x] = sheet[u][x] or sheet[d][x]

        sheet[pos:] = []  # remove rows after fold

    else:
        after = range(pos + 1, len(sheet[0]))  # lines after fold
        for l, r in zip(before, after):
            for y in range(len(sheet)):
                sheet[y][l] = sheet[y][l] or sheet[y][r]

        for y in range(len(sheet)):  # remove lines after fold
            sheet[y][pos:] = []

    # Part 1
    if i == 0:
        print(sum(map(sum, sheet)))

# Part 2
print_sheet()
