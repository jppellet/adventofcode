from sys import argv, exit
from utils import *
from dataclasses import dataclass
from functools import cached_property
from typing import Callable, cast

SAMPLE = len(argv) < 2 or argv[1] != "real"

Point = tuple[int, int, int]
Matrix = list[list[int]]


@dataclass
class ScannerData:
    i: int
    data: list[Point]
    data_rot: list[list[Point]]
    pos: Point = (0,0,0)


raw_data = read_lines(input_for(__file__, SAMPLE), str)

scanners: list[ScannerData] = []
current_scanner = None
for line in raw_data:
    if line.startswith("---"):
        i = int(line.split(" ")[2])
        current_scanner = ScannerData(i, [], [])
    elif len(line.strip()) == 0:
        if current_scanner is not None:
            scanners.append(current_scanner)
        else:
            raise ValueError("aaa")
        current_scanner = None
    else:
        p = cast(Point, tuple(map(int, line.split(","))))
        if current_scanner is not None:
            current_scanner.data.append(p)
        else:
            raise ValueError("aaah")
if current_scanner is not None:
    scanners.append(current_scanner)
    current_scanner = None


def mul(m: Matrix) -> Callable[[Point], Point]:
    def curried_call(p: Point) -> Point:
        a0 = m[0][0] * p[0] + m[0][1] * p[1] + m[0][2] * p[2]
        a1 = m[1][0] * p[0] + m[1][1] * p[1] + m[1][2] * p[2]
        a2 = m[2][0] * p[0] + m[2][1] * p[1] + m[2][2] * p[2]
        return (a0, a1, a2)
    return curried_call

def diff(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def neg(p: Point) -> Point:
    return (-p[0], -p[1], -p[2])

rots: list[Matrix] = [
    [
        [1, 0, 0], 
        [0, 1, 0],
        [0, 0, 1]
    ],
    [
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]],
    [
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ],
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ],
    [
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 0, -1],
        [-1, 0, 0]
    ],
    [
        [0, 0, -1],
        [0, -1, 0],
        [-1, 0, 0]
    ],
    [
        [0, -1, 0],
        [0, 0, 1],
        [-1, 0, 0]
    ],
    [
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, -1]
    ],
    [
        [-1, 0, 0],
        [0, 0, -1],
        [0, -1, 0]
    ],
    [
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ],
    [
        [-1, 0, 0],
        [0, 0, 1],
        [0, 1, 0]
    ],
    [
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ],
    [
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
    ],
    [
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ],
    [
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ],
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ],
    [
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, -1]
    ],
    [
        [0, 0, -1],
        [1, 0, 0],
        [0, -1, 0]
    ],
    [
        [0, -1, 0],
        [-1, 0, 0],
        [0, 0, -1]
    ],
    [
        [0, 0, 1],
        [-1, 0, 0],
        [0, -1, 0]
    ],
    [
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1]
    ],
    [
        [0, 0, -1],
        [-1, 0, 0],
        [0, 1, 0]
    ],
]

for s in scanners:
    # print(f"Scanner {s.i} has {len(s.data)} data:")
    for m in rots:
        rotate = mul(m)
        rotated_data = [rotate(p) for p in s.data]
        s.data_rot.append(rotated_data)


def find_overlap(data1: list[Point], data2: list[Point]) -> Point | None:
    # print("find overlap: ", data1)
    # print("            : ", data2)

    # get two points and try this offset
    offsets: set[Point] = set()
    for p1 in data1:
        for p2 in data2:
            offsets.add(diff(p1, p2))

    # print("  number of offsets:", len(offsets))
    # print("  offsets:", offsets)

    data1_set = set(data1)
    for offset in offsets:
        num_matches = 0
        # print("     trying offset", offset)
        for i, p2 in enumerate(data2):
            p2_off = add(p2, offset)
            # print("        checking", p2_off,":", p2_off in data1set)
            if p2_off in data1_set:
                num_matches += 1

        # check if we found a match with this offset
        if num_matches >= 12:
            return offset

    # no match found
    return None


# dictionary of the form (from, to) -> transform
# from: scanner to take data from
# to: scanner whose reference frame we'll transform the data to
# transform: list of rotations and translations to transform point from "from" to "to"
transforms: dict[tuple[int, int], list[tuple[Matrix, Point]]] = {}

def find_overlap_all_rotations(scan1: ScannerData, scan2: ScannerData) -> None:
    # print(rots[8])
    # find_overlap(s1.data, s2.data_rot[8])

    data1 = scan1.data
    for rotation_index, data2 in enumerate(scan2.data_rot):
        # print("rotation", r)
        offset = find_overlap(data1, data2)
        if offset is not None:
            transforms[(scan2.i, scan1.i)] = [(rots[rotation_index], offset)]
            print("  found overlap", scan1.i, scan2.i, offset)
            

for i in range(len(scanners)):
    for j in range(i + 1, len(scanners)):
        print(f"Searching from {i} to {j}")
        # do it in both directions because I'm too stupid to build
        # a proper affine transform matrix and invert it
        find_overlap_all_rotations(scanners[i], scanners[j])
        find_overlap_all_rotations(scanners[j], scanners[i])

# goal: as long as we have a transform from i to j and from j to k,
# build the transform from i to k
print("Augmenting the transition matrix")
while True:
    news = []

    keys = set(transforms.keys())
    for (from1, to1) in keys:
        for (from2, to2) in keys:
            if to1 == from2 and from1 != to2 and (from1, to2) not in keys:
                txlist1 = transforms[(from1, to1)]
                txlist2 = transforms[(from2, to2)]
                txlist = [*txlist1, *txlist2]
                news.append(((from1, to2) , txlist)) 

    if len(news) == 0:
        break
    for key, val in news:
        transforms[key] = val


# Part 1

all_points = set()

def add_points(s: ScannerData, txlist: list[tuple[Matrix, Point]]) -> None:
    for p in s.data:
        for rot, off in txlist:
            p = mul(rot)(p)
            p = add(p, off)
        all_points.add(p)

add_points(scanners[0], [])
for i in range(1, len(scanners)):
    add_points(scanners[i], transforms[(i, 0)])



print(f"{TERM_INVERT} Total number of points: {len(all_points)} {TERM_RESET}")


# Part 2

positions: list[Point] = [(0,0,0)]
for i in range(1, len(scanners)):
    txlist = transforms[(i, 0)]
    p = (0,0,0)
    for rot, off in txlist:
        p = mul(rot)(p)
        p = add(p, off)
    positions.append(p)

max_dist = 0
for i in range(len(positions)):
    for j in range(i+1, len(positions)):
        p1, p2 = positions[i], positions[j]
        dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) + abs(p2[2] - p1[2])
        if dist > max_dist:
            max_dist = dist

print(f"{TERM_INVERT} Maximum distance: {max_dist} {TERM_RESET}")
