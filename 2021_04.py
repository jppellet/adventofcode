from dataclasses import dataclass
from utils import *


@dataclass
class Cell:
    value: int
    marked: bool

    def __repr__(self) -> str:
        m = " * " if self.marked else "   "
        return f"{self.value:3}{m}"


@dataclass
class Board:
    index: int
    data: list[list[Cell]]

    def __repr__(self) -> str:
        cells = "\n".join(map(lambda row: " ".join(map(str, row)), self.data))
        return f"Board {self.index}:\n" + cells

    def mark_where(self, draw: int) -> bool:
        for row in self.data:
            for cell in row:
                if cell.value == draw:
                    cell.marked = True
                    return True
        return False

    def wins(self) -> bool:
        full_row = lambda row: all(map(lambda cell: cell.marked, row))
        return any(map(full_row, self.data)) or any(map(full_row, transposed(self.data)))

    def sum_unmarked(self) -> int:
        return sum(
            sum(map(lambda cell: cell.value if not cell.marked else 0, row))
            for row in self.data
        )


lines: list[str] = read_lines(input_for(__file__))
draws = list(map(int, lines[0].split(",")))
boards: list[Board] = []

PREAMBLE_LINES = 2
LINES_PER_BOARD = 6
for i in range(((len(lines) - PREAMBLE_LINES) // LINES_PER_BOARD) + 1):
    start_line = PREAMBLE_LINES + i * LINES_PER_BOARD
    board_lines = lines[start_line : start_line + LINES_PER_BOARD - 1]
    cells = list(map(lambda l: list(map(lambda s: Cell(int(s), False), l.split())), board_lines))
    boards.append(Board(i, cells))


def run_game() -> None:
    first_has_won = False
    for draw in draws:
        has_won_indices: list[int] = []
        for i, board in enumerate(boards):
            changed = board.mark_where(draw)
            if changed and board.wins():
                has_won_indices.append(i)
                if not first_has_won:
                    print(f"First to win: {board}")
                    print(draw * board.sum_unmarked())
                    first_has_won = True
                if len(boards) == 1:
                    print(f"Last to win: {board}")
                    print(draw * board.sum_unmarked())
                    return
        for i in reversed(has_won_indices):
            del boards[i]


run_game()
