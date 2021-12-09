from typing import NamedTuple
from functools import reduce
from utils import *

class DisplayData(NamedTuple):
    samples: list[str]
    readings: list[str]

SAMPLE = False
parse = lambda line: DisplayData(*(part.split() for part in line.split("|")))
data = read_lines(input_for(__file__, SAMPLE), parse)

### Part 1

def count_unambigous(case: DisplayData) -> int:
    return count_where(lambda s: len(s) in [2, 4, 3, 7], case.readings)

print(sum(map(count_unambigous, data)))

### Part 2

def decode_line(case: DisplayData) -> int:
    def digits_for_unambigous_len(n: int) -> set[str]:
        return set(find_where(lambda s: len(s) == n, case.samples)) # type: ignore

    def common_digits_for_len(n: int) -> set[str]:
        samples = map(set, find_all_where(lambda s: len(s) == n, case.samples)) # type: ignore
        return reduce(lambda a, b: a & b, samples) # type: ignore

    [c_f, b_d_c_f, a_c_f, all] = map(digits_for_unambigous_len, [2, 4, 3, 7])
    a_b_f_g = common_digits_for_len(6)
    b_d = b_d_c_f - c_f

    [a] = a_c_f - c_f
    [b] = b_d & a_b_f_g
    [d] = b_d - set([b])
    [f] = c_f & a_b_f_g
    [c] = c_f - set([f])
    [g] = a_b_f_g - set([a, b, f])
    [e] = all - set([a, b, c, d, f, g])

    sets = list(map(set, [ # type: ignore
        [a, b, c, e, f, g],
        [c, f],
        [a, c, d, e, g],
        [a, c, d, f, g],
        [b, c, d, f],
        [a, b, d, f, g],
        [a, b, d, e, f, g],
        [a, c, f],
        [a, b, c, d, e, f, g],
        [a, b, c, d, f, g],
    ]))

    max_index = len(case.readings) - 1
    def decode_digit(pos_digits: tuple[int, str]) -> int:
        radix: int = 10 ** (max_index - pos_digits[0])
        pat_set = set(pos_digits[1])
        return radix * index_where(lambda s: s == pat_set, sets)

    return sum(map(decode_digit, enumerate(case.readings)))

print(sum(map(decode_line, data)))