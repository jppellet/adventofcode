from utils import *

depths = read_lines(input_for(__file__), int)
paired_depths = list(zip(depths, depths[1:]))
larger = lambda pair: pair[1] - pair[0] > 0
print(count_where(larger, paired_depths))

sliding_sum = list(map(sum, zip(depths, depths[1:], depths[2:])))
paired_sums = list(zip(sliding_sum, sliding_sum[1:]))
print(count_where(larger, paired_sums))
