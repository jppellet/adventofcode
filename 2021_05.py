from typing import Tuple
from utils import *

Point = Tuple[int, int]
Board = list[list[int]]


def parse_coords(line: str) -> Tuple[Point, Point]:
    p1, p2 = line.split(" -> ")
    x1, y1 = map(int, p1.split(","))
    x2, y2 = map(int, p2.split(","))
    return (x1, y1), (x2, y2)


def print_board(board: Board) -> None:
    for row in board:
        print("".join(map(str, ["." if c == 0 else str(c) for c in row])))


def count_overlapping(with_diags: bool = False) -> int:
    board = [[0 for _ in range(width)] for _ in range(height)]
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                board[y][x1] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                board[y1][x] += 1
        elif with_diags and (diff := abs(y2 - y1)) == abs(x2 - x1):
            dx = sign(x2 - x1)
            dy = sign(y2 - y1)
            for _ in range(diff + 1):
                board[y1][x1] += 1
                x1 += dx
                y1 += dy
    return sum(map(lambda line: count_where(lambda i: i > 1, line), board))


lines = read_lines(input_for(__file__), parse_coords)
width = max(max(x1, x2) for (x1, _), (x2, _) in lines) + 1
height = max(max(y1, y2) for (_, y1), (_, y2) in lines) + 1
print(count_overlapping(with_diags=False))
print(count_overlapping(with_diags=True))
