from sys import argv
from typing import NamedTuple, Generator
from functools import cache
from utils import *

SAMPLE = len(argv) < 2 or argv[1] != "real"
start_positions = [4, 8] if SAMPLE else [1, 5]


# Part 1

def make_die() -> Generator[int, None, None]:
    while True:
        for i in range(1, 101):
            yield i

die = make_die()
positions = start_positions[:]
scores = [0, 0]
p = -1
num_turns = 0

while True:
    p = (p + 1) % 2
    num_turns += 1
    roll = next(die) + next(die) + next(die)
    newpos = 1 + (((positions[p] - 1) + roll) % 10)
    positions[p] = newpos
    scores[p] += newpos
    if scores[p] >= 1000:
        result = num_turns * 3 * scores[(p + 1) % 2]
        print_result(result)
        break


# Part 2

class GameState(NamedTuple):
    nextplayer_pos: int
    nextplayer_score: int
    prevplayer_pos: int
    prevplayer_score: int

def possible_rolls() -> Generator[int, None, None]:
    roll_range = [1, 2, 3]
    for r1 in roll_range:
        for r2 in roll_range:
            for r3 in roll_range:
                yield r1 + r2 + r3

@cache
def compute_wins_from_state(state: GameState) -> tuple[int, int]:
    """
    Recursively compute the number of possible wins from a given state.
    This is cached to avoid recomputing the same thing over and over.
    The next player alternates between Player 1 and Player 2.
    """
    num_wins = [0, 0] # current player always first, but this is not always Player 1
    for roll in possible_rolls():
        newpos = (state.nextplayer_pos - 1 + roll) % 10 + 1
        newscore = state.nextplayer_score + newpos
        if newscore >= 21: # win, stop evaluating this branch
            num_wins[0] += 1
        else: # no win, go on playing
            newstate = GameState(
                state.prevplayer_pos, state.prevplayer_score,
                newpos, newscore,
            )
            subwins = compute_wins_from_state(newstate)
            # inverted because the next player is the other one
            num_wins[0] += subwins[1]
            num_wins[1] += subwins[0]
    return num_wins[0], num_wins[1]

wins = compute_wins_from_state(GameState(start_positions[0], 0, start_positions[1], 0))
print_result(f"Max wins: {max(wins)}")
