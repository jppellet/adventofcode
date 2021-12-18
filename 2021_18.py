from sys import argv
from typing import Any, Tuple
from utils import *
from functools import reduce
from dataclasses import dataclass

SAMPLE = len(argv) < 2 or argv[1] != "real"
all_fish = read_lines(input_for(__file__, SAMPLE), eval)

@dataclass
class Cell:
    """
    Models as an int cell in a doubly-linked list. Such cells are used to
    have a flat representation of the possibly nested snailfish values.
    """
    v: int
    prev: Optional["Cell"] = None
    next: Optional["Cell"] = None

    def __repr__(self) -> str:
        return str(self.v)


def make_cells(l: list) -> list:
    """
    From nested lists of numbers, produces the same nested list of cells,
    linking the cells together.
    """
    latest_made_cell: Optional[Cell] = None
    def mkcells_rec(l: list | int) -> list | Cell:
        nonlocal latest_made_cell
        if islist(l): # recurse
            return list(map(mkcells_rec, l)) # type: ignore
        # make cell and link it to previous
        new_cell = Cell(l) # type: ignore
        if latest_made_cell is not None:
            latest_made_cell.next = new_cell
            new_cell.prev = latest_made_cell
        latest_made_cell = new_cell
        return new_cell

    return mkcells_rec(l) # type: ignore


def flatten_cells(l: list | Cell) -> list | int:
    """
    From nested lists of cells, produces back a nested list of numbers.
    """
    if islist(l):
        return list(map(flatten_cells, l)) # type: ignore
    return l.v # type: ignore


def try_explode(l_0: list) -> Tuple[list, bool]:
    """
    Tries to make the explode operation. The second returned value is False
    if nothing could be exploded.
    """
    exploded_already = False
    def explode_rec(l: list, depth: int) -> list:
        nonlocal exploded_already
        new: list = []
        for e in l:
            if islist(e):
                if not exploded_already and depth == 3:
                    left, right = e
                    new_cell = Cell(0)
                    if left.prev is not None:
                        left.prev.v += left.v
                        new_cell.prev = left
                        left.next = new_cell
                    if right.next is not None:
                        right.next.v += right.v
                        new_cell.next = right
                        right.prev = new_cell
                    new.append(new_cell)
                    exploded_already = True
                else:
                    new.append(explode_rec(e, depth + 1))
            else:  # number
                new.append(e)
        return new

    return explode_rec(l_0, 0), exploded_already


def try_split(l: list) -> Tuple[list, bool]:
    """
    Tries to split a number somewhere. The second returned value is False
    if nothing could be split.
    """
    split_already = False
    def split_rec(l: list) -> Any:
        nonlocal split_already
        new = []
        for e in l:
            if islist(e):
                new.append(split_rec(e))
            else:  # number
                if not split_already and e >= 10:
                    halfdown = e // 2
                    new.append([halfdown, e - halfdown])
                    split_already = True
                else:
                    new.append(e)
        return new

    return split_rec(l), split_already

def add(fish1: list, fish2: list) -> list:
    new_fish = [fish1, fish2]
    while True:
        # try to explode
        new_fish_cells = make_cells(new_fish)
        exploded, changed = try_explode(new_fish_cells)
        if changed:
            new_fish = flatten_cells(exploded) # type: ignore
            continue

        # try to split
        splitted, changed = try_split(new_fish)
        if changed:
            new_fish = splitted
        else:
            break
    return new_fish



def magnitude(fish: list | int) -> int:
    if not islist(fish):
        return fish # type: ignore
    return 3 * magnitude(fish[0]) + 2 * magnitude(fish[1]) # type: ignore


# Part 1

print(magnitude(reduce(add, all_fish)))


# Part 2

max_magn = 0
it = 0 # goes up to 9900
for f1 in all_fish:
    for f2 in all_fish:
        if f1 is not f2:
            it += 1
            if it % 100 == 0:
                print(f"  {it=}...")
            for magn in [ magnitude(add(f1, f2)),  magnitude(add(f2, f1))]:
                if magn > max_magn:
                    max_magn = magn

print(max_magn)
