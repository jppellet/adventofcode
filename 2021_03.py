from typing import Tuple
from utils import *

Counts = Tuple[int, int]

bins = read_lines(input_for(__file__))
width = len(bins[0])


def count_bits_at(i: int, rows: list[str]) -> Counts:
    bits = list(map(lambda b: b[i], rows))
    num_0 = bits.count("0")
    num_1 = len(rows) - num_0
    return num_0, num_1


def part1():
    gamma_str = ""
    epsilon_str = ""
    for i in range(width):
        num_0, num_1 = count_bits_at(i, bins)
        gamma_digit = 1 if num_1 > num_0 else 0
        epsilon_digit = (gamma_digit + 1) % 2
        gamma_str += str(gamma_digit)
        epsilon_str += str(epsilon_digit)

    gamma = int(gamma_str, 2)
    epsilon = int(epsilon_str, 2)
    print(gamma * epsilon)


def filter_loop(to_keep: Callable[[Counts], str]) -> int:
    candidates = bins[:]
    for i in range(width):
        filter_bit = to_keep(count_bits_at(i, candidates))
        candidates = [c for c in candidates if c[i] == filter_bit]
        if len(candidates) == 1:
            break
    return int(candidates[0], 2)


def part2():
    o2_gen = filter_loop(lambda nums: "1" if nums[1] >= nums[0] else "0")
    co2_scrub = filter_loop(lambda nums: "0" if nums[0] <= nums[1] else "1")
    print(o2_gen * co2_scrub)


part1()
part2()
