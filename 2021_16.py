from sys import argv
from typing import Any
from math import prod
import operator as op
from utils import *

SAMPLE = len(argv) < 2 or argv[1] != "real"

raw = read_lines(input_for(__file__, SAMPLE), str)[0]

hex2bin = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111",
}

bin = "".join([hex2bin[c] for c in raw])

def bin2dec(bin: str) -> int:
    return int(bin, 2)

pos = 0
def grab(n: int) -> str:
    global pos
    res = bin[pos:pos + n]
    pos += n
    return res

sum_versions = 0
LIT = "lit"
SUB = "sub"

def parse_packet(indent: str) -> tuple[str, int, Any]:
    global sum_versions
    start_pos = pos
    version = bin2dec(grab(3))
    sum_versions += version
    id = bin2dec(grab(3))

    if id == 4: # literal
        buf = ""
        while grab(1) == "1":
            buf += grab(4)
        buf += grab(4)
        n = bin2dec(buf)
        read = pos - start_pos
        print(indent + LIT + f"({n}) on {read} bits")
        return LIT, n, None

    else: # subpackets
        print(indent + SUB + f"(id: {id})")
        sub_pkts = []
        len_type = grab(1)
        if len_type == "0":
            total_length = bin2dec(grab(15))
            stop_when = pos + total_length
            while pos < stop_when:
                pkt = parse_packet(indent + "  ")
                sub_pkts.append(pkt)
        else:
            n_sub = bin2dec(grab(11))
            for _ in range(n_sub):
                pkt = parse_packet(indent + "  ")
                sub_pkts.append(pkt)
        return SUB, id, sub_pkts

pkt = parse_packet("  ")
print(f"vs: {sum_versions}")

Func = Callable[[list[int]], int]

def func_from(op: Callable[[int, int], int]) -> Func:
    return lambda args: op(args[0], args[1])

funcs: dict[int, Func] = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: func_from(op.gt),
    6: func_from(op.lt),
    7: func_from(op.eq),
}

def eval(pkt: tuple[str, int, Any]) -> int:
    type, n, subs = pkt
    if type == LIT:
        return n
    elif type == SUB:
        vals = list(map(eval, subs))
        return funcs[n](vals)
    return -1

print(eval(pkt))