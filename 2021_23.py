from sys import argv, exit
from typing import NamedTuple
from utils import *

SAMPLE = len(argv) < 2 or argv[1] != "real"

Position = tuple[int, int]
class Move(NamedTuple):
    from_pos: Position
    to_pos: Position
    cost: int

def print_grid() -> None:
    print("      ", end="")
    for i in range(11):
        print(f" {i} ", end="")
    print()
    for y in range(-1, depth + 2):
        print(f"{y}  " if 0 <= y <= depth else "   ", end="")
        for x in range(-1, 12):
            pos = (x, y)
            if not pos in grid:
                print("###", end="")
            else:
                l = grid[pos]
                if l is None:
                    print(" . ", end="")
                else:
                    print(" " + l + " ", end="")
        print()
    print("--")


dest_cols = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}
room_cols = list(dest_cols.values())
blacklist = list(map(lambda c: (c, 0), room_cols))
top_range = [pos for x in range(11) if (pos := (x, 0)) not in blacklist]
costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

def is_finished() -> bool:
    for x in room_cols:
        for y in range(1, depth + 1):
            l = grid[(x, y)]
            if l is None:
                return False
            if dest_cols[l] != x:
                return False
    return True

def do_move(from_pos: Position, to_pos: Position) -> None:
    grid[to_pos] = grid[from_pos]
    grid[from_pos] = None

def make_path(from_pos: Position, to_pos: Position) -> list[Position]:
    if from_pos == to_pos:
        return []
    path: list[Position] = []
    if from_pos[1] == 0:
        # into room, horizontal first
        dir = sign(to_pos[0] - from_pos[0])
        if dir != 0:
            next_x = from_pos[0] + dir * 1
            after_last_x = to_pos[0] + dir * 1
            # horizontal
            for x in range(next_x, after_last_x, dir):
                path.append((x, 0))
        # then down
        for y in range(1, to_pos[1] + 1):
            path.append((to_pos[0], y))
    else:
        # out of room, vertical first
        for y in range(from_pos[1] - 1, -1, -1):
            path.append((from_pos[0], y))
        # then horizontally
        dir = sign(to_pos[0] - from_pos[0])
        if dir != 0:
            next_x = from_pos[0] + dir * 1
            after_last_x = to_pos[0] + dir * 1
            for x in range(next_x, after_last_x, dir):
                path.append((x, 0))
        # then down if needed
        for y in range(1, to_pos[1] + 1):
            path.append((to_pos[0], y))
    return path

def is_path_free(from_pos: Position, to_pos: Position) -> tuple[bool, int]:
    path = make_path(from_pos, to_pos)
    # print(f"trying to move from {from_pos} to {to_pos} with path {path}")
    for pos in path:
        if grid[pos] is not None:
            # print(f"blocked at {(x, 0)}")
            return False, 0
    return True, len(path)

def list_moves() -> list[Move]:
    moves: list[Move] = []

    def add_move(from_pos: Position, to_pos: Position, length: int) -> None:
        l = grid[from_pos]
        if l is None:
            raise ValueError("moving empty cell")
        unit_cost = costs[l]
        moves.append(Move(from_pos, to_pos, length * unit_cost))

    def add_move_if_path_free(from_pos: Position, to_pos: Position) -> None:
        free, length = is_path_free(from_pos, to_pos)
        if free:
            # print(f" >> {to_pos}")
            add_move(from_pos, to_pos, length)

    for pos in top_range:
        # print(f"checking moves from {pos}")
        l = grid[pos]
        if l is None:
            continue
        dest_col = dest_cols[l]
        if grid[(dest_col, 1)] is None:
            # there's room there
            y = 1
            while y < depth and grid[(dest_col, y + 1)] is None:
                # go down
                y += 1

            if y == depth:
                # bottom
                add_move_if_path_free(pos, (dest_col, y))
            else:
                # check all the rest are of the same type
                all_same = True
                for yy in range(y + 1, depth + 1):
                    if grid[(dest_col, yy)] != l:
                        all_same = False
                        break
                if all_same:
                    add_move_if_path_free(pos, (dest_col, y))

    for x in room_cols:
        # look for top one in this col
        y = 1
        while y <= depth and (l := grid[(x, y)]) is None:
            y += 1
        other_down = False
        for yy in range(y + 1, depth + 1):
            if grid[(x, yy)] != l:
                other_down = True
                break

        if l is not None:
            # print(f"col={x}, found {l} at y={y} -- {other_down=}")
            if dest_cols[l] != x or other_down:
                # print(f"in col {x}: {l} at y={y}")
                # try to get it out to the top row
                from_pos = (x, y)
                for to_pos in top_range:
                    add_move_if_path_free(from_pos, to_pos)
    return moves


def print_moves(moves: list[Move]) -> None:
    print("-- BEGIN MOVES")
    for i, move in enumerate(moves):
        print(f"{(i+1):3}. Move {move.from_pos} to {move.to_pos} (cost = {move.cost})")
    print("-- END MOVES")

best_cost = float("inf")
best_moves: list[Move] = []

def play_next_moves(cum_cost: int, past_moves: list[Move]) -> None:
    global best_cost
    if cum_cost >= best_cost:
        return

    if interactive:
        print_grid()
    if is_finished():
        if cum_cost < best_cost:
            best_cost = cum_cost
            best_moves = past_moves
            print_result(f"found new solution with cost {cum_cost}")
            print_moves(best_moves)
        return

    if interactive:
        input("Enter to go on...")
    moves = list_moves()
    if interactive and len(moves) == 0:
        print("dead end")
    for move in sorted(moves, key=lambda m: m.cost):
        from_pos, to_pos, cost = move
        do_move(from_pos, to_pos)
        play_next_moves(cum_cost + cost, [*past_moves, move])
        do_move(to_pos, from_pos)


grid_part1 = {
    (0, 0): None,
    (1, 0): None,
    (2, 0): None,
    (3, 0): None,
    (4, 0): None,
    (5, 0): None,
    (6, 0): None,
    (7, 0): None,
    (8, 0): None,
    (9, 0): None,
    (10, 0): None,
    (2, 1): "D",
    (2, 2): "C",
    (4, 1): "B",
    (4, 2): "A",
    (6, 1): "C",
    (6, 2): "D",
    (8, 1): "A",
    (8, 2): "B",
}

grid_part2 = {
    (0, 0): None,
    (1, 0): None,
    (2, 0): None,
    (3, 0): None,
    (4, 0): None,
    (5, 0): None,
    (6, 0): None,
    (7, 0): None,
    (8, 0): None,
    (9, 0): None,
    (10, 0): None,
    (2, 1): "D",
    (2, 2): "D",
    (2, 3): "D",
    (2, 4): "C",
    (4, 1): "B",
    (4, 2): "C",
    (4, 3): "B",
    (4, 4): "A",
    (6, 1): "C",
    (6, 2): "B",
    (6, 3): "A",
    (6, 4): "D",
    (8, 1): "A",
    (8, 2): "A",
    (8, 3): "C",
    (8, 4): "B",
}

grid = grid_part1 if SAMPLE else grid_part2
depth = max(map(lambda pos: pos[1], grid.keys()))

interactive = False

play_next_moves(cum_cost=0, past_moves=[])
print("Nothing more to find")
