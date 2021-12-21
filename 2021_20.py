from sys import argv, exit
from utils import *
from itertools import starmap

SAMPLE = len(argv) < 2 or argv[1] != "real"

data = read_lines(input_for(__file__, SAMPLE), str)
refline = [char == "#" for char in data[0]]
img = [[int(char == "#") for char in row] for row in data[2:]]
padding = (
    10  # pixels in the "inifite region" may alternate; the margin has to be big enough
)


def neighborhood(x: int, y: int) -> list[tuple[int, int]]:
    xs = range(x - 1, x + 2)
    ys = range(y - 1, y + 2)
    coords = [(_x, _y) for _y in ys for _x in xs]
    if any(map(lambda a: a < 0, (a for p in coords for a in p))):
        print(f"ERROR smaller than 0: {x} {y}")
    return coords


def step() -> None:
    global img
    expanded_img = []

    for _ in range(padding):  # pad top
        expanded_img.append([0] * (len(img[0]) + 2 * padding))
    for row in img:
        expanded_img.append([0] * padding + row + [0] * padding)
    for _ in range(padding):  # pad bottom
        expanded_img.append([0] * (len(img[0]) + 2 * padding))

    new_img = [[0] * (len(expanded_img[0]) - 2) for _ in range(len(expanded_img) - 2)]
    for y in range(1, len(expanded_img) - 1):
        for x in range(1, len(expanded_img[y]) - 1):
            pixels9 = [expanded_img[y_][x_] for x_, y_ in neighborhood(x, y)]
            refindex = int("".join(map(lambda a: str(int(a)), pixels9)), 2)
            new_img[y - 1][x - 1] = refline[refindex]

    img = new_img


def print_image() -> None:
    for row in img:
        print("".join(map(lambda a: "#" if a else ".", row)))
    print("\n--\n")


for i in range(25):
    # we actually can't count after any odd step because there will be
    # infinitely many lit pixels
    for _ in range(2):
        step()
        # print_image()
    print(i)
    
    # keep size manageable
    trim = 2 * padding - 4
    img = img[trim:-trim]
    img = [row[trim:-trim] for row in img]
    if i == 0 or i == 24:
        print(f"{TERM_INVERT} After {(i+1)*2} steps: {sum(map(sum, img))} {TERM_RESET}")