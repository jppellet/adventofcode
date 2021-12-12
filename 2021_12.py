from collections import defaultdict
from utils import *

SAMPLE = False

data = read_lines(input_for(__file__, SAMPLE), lambda line: line.split("-"))
G: dict[str, set[str]] = defaultdict(set)
for n1, n2 in data:
    G[n1].add(n2)
    G[n2].add(n1)

def walk(paths: list[str], visited: list[str], joker_used: bool) -> None:
    for n in G[visited[-1]]:
        if n == "end":
            paths.append(",".join([*visited, n]))
        elif n == "start":
            continue
        elif n.isupper() or n not in visited:
            walk(paths, [*visited, n], joker_used)
        elif not joker_used:
            walk(paths, [*visited, n], True)

def solve(allow_joker: bool) -> None:
    paths: list[str] = []
    walk(paths, ["start"], not allow_joker)
    print(len(paths))

solve(allow_joker=False)
solve(allow_joker=True)
