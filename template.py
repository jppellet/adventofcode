from sys import argv, exit
from utils import *

SAMPLE = len(argv) < 2 or argv[1] != "real"

data = read_lines(input_for(__file__, SAMPLE), str)
# data = read_first_line(input_for(__file__, SAMPLE), ",", str)

_t = 0
def print_data() -> None:
    global _t
    print(f"Data at time {_t}:")
    for line in data:
        print(line)
    print("----\n")
    _t += 1


print_data()

print_result("--")