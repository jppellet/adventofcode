from utils import *

SAMPLE = False
ints = read_lines(input_for(__file__, SAMPLE), int)

print(ints)

for i in ints:
    for j in ints:
        if i + j == 2020:
            print(i * j)

for i in ints:
    for j in ints:
        for k in ints: 
            if i + j + k == 2020:
                print(i * j * k)