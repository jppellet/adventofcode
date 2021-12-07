from utils import *

SAMPLE = False
data = read_first_line(input_for(__file__, SAMPLE), ",", int)

MAX = 9
nums = [data.count(d) for d in range(MAX)]
for i in range(256):
    nums[(i + 7) % MAX] += nums[i % MAX]
    if i == 79 or i == 255:
        print(f"After {i+1:3} days: {sum(nums)}")