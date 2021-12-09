from utils import *

SAMPLE = False
lines = read_lines(input_for(__file__, SAMPLE), str)

def is_valid(line: str) -> bool:
    [range,letter,password] = line.split(" ")
    letter = letter[0]
    [from_str, to_str] = range.split("-")
    from_int = int(from_str)
    to_int = int(to_str)
    count = password.count(letter)
    at_first = password[from_int-1] == letter
    at_second = password[to_int-1] == letter
    return (at_first or at_second) and not (at_first and at_second)

n = 0
for line in lines:
    if is_valid(line):
        n += 1

print(n)