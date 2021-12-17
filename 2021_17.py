from sys import argv, exit
from utils import *

SAMPLE = len(argv) < 2 or argv[1] != "real"

if SAMPLE:
    x_min, x_max = 20, 20
    y_min, y_max = -10, -5

else:
    x_min, x_max = 117, 164
    y_min, y_max = -140, -89


x_t = range(x_min, x_max+1)
y_t = range(y_min, y_max+1)

def hits(x: int, y: int) -> bool:
    return x in x_t and y in y_t

def is_over(x: int, y: int) -> bool:
    return x > x_max or y < y_min

def throw(vx: int, vy: int) -> int:
    x, y = 0, 0
    max_height = y
    while True:
        x += vx
        y += vy
        if y > max_height:
            max_height = y
        if hits(x, y):
            return max_height
        if is_over(x, y):
            return -1
        vx -= sign(vx)
        vy -= 1
    raise ValueError("aaah")

def find_minvx() -> int:
    vx = 1
    while True:
        final_possible_x = vx * (vx+1) // 2
        if final_possible_x >= x_min:
            return vx
        vx += 1

minvx = find_minvx()
maxvx = x_max
vxrange = range(minvx, maxvx + 1)

maxvy = 1000 # wild guess
vyrange = range(y_min, maxvy + 1)

max_height = -1
best_v = -1, -1
num_found = 0
for vx in vxrange:
    for vy in vyrange: 
        height = throw(vx, vy)
        if height != -1:
            num_found += 1
            if height > max_height:
                max_height = height
                best_v = vx, vy
                print(f"{height}: {vx} {vy} ")

print(num_found, max_height, best_v)
