from utils import *
from sys import exit, argv
from collections import Counter

SAMPLE = len(argv) < 2 or argv[1] != "real"

data = read_lines(input_for(__file__, SAMPLE), str)
start = data[0]
first_char, last_char = start[0], start[-1]
rules = {p: i for p, i in [line.split(" -> ") for line in data[2:]]}

pair_counter = Counter(map(lambda p: "".join(p), zip(start, start[1:])))

def count_elems() -> Counter[str]:
    counts: Counter[str] = Counter()
    for key, c in pair_counter.items():
        for elem in key:
            counts[elem] += c
    counts[first_char] += 1
    counts[last_char] += 1
    for elem, count in counts.items():
        counts[elem] = count // 2
    return counts

def step() -> None:
    global pair_counter
    newcounts: Counter[str] = Counter()
    for pair, n in pair_counter.items():
        ins = rules[pair]
        newcounts[pair[0] + ins] += n
        newcounts[ins + pair[1]] += n
    pair_counter = newcounts

def print_result() -> None:
    counts = list(count_elems().values())
    print(max(counts) - min(counts))

for runs in 10, 30:
    for _ in range(runs):
        step()
    print_result()