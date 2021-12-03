from utils import *
from functools import reduce

trees = read_lines("2020_3.txt", lambda line: [c == "#" for c in line])


def count_trees(right: int, down: int) -> int:
    print(f"Counting with offset {right} {down}... ", end="")
    n_trees = 0

    print(f"lines: {len(list(range(0, len(trees), down)))}", end="")

    for i in range(0, len(trees), down):
        print(i, " ", end="")
        if trees[i][((i//down) * right) % len(trees[i])]:
            n_trees += 1

    print("Trees:", n_trees)
    return n_trees


cases = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

res = reduce(lambda acc, case: acc * count_trees(*case), cases, 1)

print(res)
