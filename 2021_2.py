from typing import Tuple
from utils import *

def parse_line(line: str) -> Tuple[str, int]:
    [cmd, arg_str] = line.split(" ")
    return cmd, int(arg_str)

instrs = read_lines(input_for(__file__), parse_line)

def part1():
    hpos = 0
    depth = 0
    for instr in instrs:
        match instr:
            case ("forward", x):
                hpos += x
            case ("down", x):
                depth += x
            case ("up", x):
                depth -= x

    print(hpos * depth)

def part2():
    hpos = 0
    depth = 0
    aim = 0
    for instr in instrs:
        match instr:
            case ("down", x):
                aim += x
            case ("up", x):
                aim -= x
            case ("forward", x):
                hpos += x
                depth += aim * x

    print(hpos * depth)

part1()
part2()