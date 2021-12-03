from typing import Tuple
from utils import *

def parse_instr(line: str) -> Tuple[str, int]:
    cmd, arg_str = line.split()
    return cmd, int(arg_str)

instrs = read_lines(input_for(__file__), parse_instr)

def part1():
    hpos = 0
    depth = 0
    for cmd, arg in instrs:
        match cmd:
            case "forward":
                hpos += arg
            case "down":
                depth += arg
            case "up":
                depth -= arg

    print(hpos * depth)

def part2():
    hpos = 0
    depth = 0
    aim = 0
    for cmd, arg in instrs:
        match cmd:
            case "down":
                aim += arg
            case "up":
                aim -= arg
            case "forward":
                hpos += arg
                depth += aim * arg

    print(hpos * depth)

part1()
part2()