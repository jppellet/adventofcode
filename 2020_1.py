from utils import *

ints = read_lines("2020_1.txt", int)

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