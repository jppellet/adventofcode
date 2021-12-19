
from math import pi, cos, sin
from utils import sign
from typing import Callable, cast

pi2 = pi / 2
angles = [0, pi2, pi, 3 * pi2]

Point = tuple[int, int, int]
Matrix = list[list[int]]

rots: list[Matrix] = []
for alpha in angles:
    for beta in angles:
        for gamma in angles:
            m = [
                [cos(alpha) * cos(beta), cos(alpha)*sin(beta)*sin(gamma) - sin(alpha)*cos(gamma), cos(alpha)*sin(beta)*cos(gamma) + sin(alpha)*sin(gamma)],
                [sin(alpha) * cos(beta), sin(alpha)*sin(beta)*sin(gamma) + cos(alpha)*cos(gamma), sin(alpha)*sin(beta)*cos(gamma)-cos(alpha)*sin(gamma)],
                [-sin(beta),             cos(beta)*sin(gamma),                                    cos(beta)*cos(gamma)],
            ]
            for r in m:
                for i, v in enumerate(r):
                    if abs(v) < 0.00001:
                        r[i] = 0
                    elif abs(v) - 1 < 0.00001:
                        r[i] = int(1 * sign(v))
            if m not in rots:
                rots.append(cast(Matrix, m))



def print_matrix(m: Matrix) -> None:
    print("[")
    for row in m:
        print("  ", row, ",", sep="")
    print("],\n")


p = (1, 2, 3)

def mul(m: Matrix) -> Callable[[Point], Point]:
    def curried_call(p: Point) -> Point:
        a0 = m[0][0] * p[0] + m[0][1] * p[1] + m[0][2] * p[2]
        a1 = m[1][0] * p[0] + m[1][1] * p[1] + m[1][2] * p[2]
        a2 = m[2][0] * p[0] + m[2][1] * p[1] + m[2][2] * p[2]
        return (a0, a1, a2)
    return curried_call


for mat in rots:
    print_matrix(mat)

print(len(rots))
