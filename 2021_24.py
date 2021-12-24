# from sys import argv, exit
# from dataclasses import dataclass, field
# from utils import *

# SAMPLE = len(argv) < 2 or argv[1] != "real"
# data = read_first_line(input_for(__file__, SAMPLE), ",", str)

# W = 0
# X = 1
# Y = 2
# Z = 3

# @dataclass
# class ALU:
#     whole_input: list[int]
#     next_input_index: int = 0
#     regs: list[int] = field(default_factory=lambda: [0, 0, 0, 0])

#     def __repr__(self) -> str:
#         return f"ALU(w={self.regs[W]}, x={self.regs[X]}, y={self.regs[Y]}, z={self.regs[Z]};  next_input_index={self.next_input_index}, whole_input={self.whole_input})"

# def inp(alu: ALU, regi: int, __unused: int) -> None:
#     alu.regs[regi] = alu.whole_input[alu.next_input_index]
#     alu.next_input_index += 1

# def nop(__unused0: ALU, __unused1: int, __unused2: Any) -> None:
#     pass

# def add(alu: ALU, regi: int, regj: int) -> None:
#     alu.regs[regi] += alu.regs[regj]

# def addi(alu: ALU, regi: int, imm: int) -> None:
#     alu.regs[regi] += imm

# def mul(alu: ALU, regi: int, regj: int) -> None:
#     alu.regs[regi] *= alu.regs[regj]

# def muli(alu: ALU, regi: int, imm: int) -> None:
#     alu.regs[regi] *= imm

# def div(alu: ALU, regi: int, regj: int) -> None:
#     alu.regs[regi] //= alu.regs[regj]

# def divi(alu: ALU, regi: int, imm: int) -> None:
#     alu.regs[regi] //= imm

# def mod(alu: ALU, regi: int, regj: int) -> None:
#     alu.regs[regi] %= alu.regs[regj]

# def modi(alu: ALU, regi: int, imm: int) -> None:
#     alu.regs[regi] %= imm

# def eql(alu: ALU, regi: int, regj: int) -> None:
#     alu.regs[regi] = int(alu.regs[regi] == alu.regs[regj])

# def eqli(alu: ALU, regi: int, imm: int) -> None:
#     alu.regs[regi] = int(alu.regs[regi] == imm)

# reg_names = ["w", "x", "y", "z"]
# instr_names = ["inp", "add", "mul", "div", "mod", "eql"]
# instr_impls: list[Callable[[ALU, int, int], None]] = [
#     inp,  # 0
#     nop,
#     add,  # 2
#     addi,
#     mul,  # 4
#     muli,
#     div,  # 6
#     divi,
#     mod,  # 8
#     modi,
#     eql,  # 10
#     eqli,
# ]

# Instr = tuple[int, int, int]
# Program = list[Instr]

# def compile(data: list[list[str]]) -> Program:
#     def compile_instr(line: list[str]) -> Instr:
#         instr_ind = 2 * instr_names.index(line[0])
#         regi = reg_names.index(line[1])
#         if len(line) > 2:
#             try:
#                 arg2 = int(line[2])
#                 instr_ind += 1  # immediate version
#             except ValueError as err:
#                 arg2 = reg_names.index(line[2])
#         else:
#             arg2 = 0
#         return instr_ind, regi, arg2

#     return list(map(compile_instr, data))


# program = compile(data)
# print(f"Program has {len(program)} instrs")

# def run_alu(inputs: list[int]) -> tuple[bool, int]:
#     alu = ALU(inputs)
#     for i, (instr_ind, regi, arg2) in enumerate(program):
#         try:
#             instr_impls[instr_ind](alu, regi, arg2)
#         except IndexError:
#             print(f"ERROR on line {i+1}")
#             print(f"state: {alu}")
#             raise
#     valid = alu.regs[Z] == 0
#     return valid, alu.regs[Z]

# NO: the whole thing above is useless because it takes too
# damn long to run, even if written in C

from itertools import accumulate
import operator as op
from utils import *

# extracted arguments to the operators changing between input digits
inf = float("inf")
divz_list = [1, 1, 1, 1, 1, 26, 1, 26, 26, 1, 26, 26, 26, 26]
addx_list = [10, 12, 10, 12, 11, -16, 10, -11, -13, 13, -8, -1, -4, -14]
addy_list = [12, 7, 8, 8, 15, 12, 8, 13, 3, 13, 3, 9, 4, 13]

# this is the maximum value z can have at each step if we hope to see it each zero at the end. It get divided by the values in divz_list at each step, so if it is any greater that the product of all remaining divisors, no need to go on.
max_z_by_step = list(accumulate(divz_list[::-1], op.mul, initial=1))[::-1]
# print(f"{max_z_by_step=}")

# simple function version of what the ALU does at each step
def checksum_digit(prev_z: int, digit: int, divz: int, addx: int, addy: int) -> int:
    if (prev_z % 26 + addx) != digit:
        return prev_z // divz * 26 + digit + addy
    else:
        return prev_z // divz

Cache = dict[int, tuple[int, int]]

# Idea: each step crunching one more digit can only lead to a finite number of z, with which a single min and max input can be associated. So instead of caching a z for possible inputs or subinputs, we cache the min and max input for each z.
# We go though digits and for each prefix of len=1, 2, ... we keep the largest and the smallest input leading to an given z.
# Then, at the next step, we only need to add digits starting with all possible values of previous z and for each such z the two linked inputs.

# initial cache: accumulator z is zero; min and max input
# leading to this are both zero as well
best_input_by_z: Cache = {0: (0, 0)}

pbar_length = 50
for pos in range(14):

    length = len(best_input_by_z)
    print(f"Determining values for digit {pos + 1}... ({length} steps)")
    pbar_shown = 0

    # extract arguments for this position
    divz = divz_list[pos]
    addx = addx_list[pos]
    addy = addy_list[pos]
    max_z = max_z_by_step[pos]

    # this new cache will only contain z values obtained after
    # updating the checksum of one more digit
    new_best_input_by_z: Cache = {}

    for i, (prev_z, prev_inputs) in enumerate(best_input_by_z.items()):
        for digit in range(1, 10):

            new_z = checksum_digit(prev_z, digit, divz, addx, addy)
            if new_z >= max_z:
                continue

            new_min, new_max = map(lambda prev: prev * 10 + digit, prev_inputs)

            old_best_input = new_best_input_by_z.get(new_z, None)
            if old_best_input is not None:
                # we have reached the same z before; see if the input we have now is better
                old_min, old_max = old_best_input
                new_min = min(new_min, old_min)
                new_max = max(new_max, old_max)
            new_best_input_by_z[new_z] = new_min, new_max

        # little progress bar to show we've not died yet
        pbar_to_show = int((i + 1) * pbar_length / length)
        print("*" * (pbar_to_show - pbar_shown), end="", flush=True)
        pbar_shown = pbar_to_show

    print() # end of pbar
    best_input_by_z = new_best_input_by_z

print_result(f"Min and max: {best_input_by_z.get(0, None)}")
