from utils import *
from sys import argv
from dataclasses import dataclass

@dataclass
class InstructionLine:
    on: bool
    rangex: tuple[int, int]
    rangey: tuple[int, int]
    rangez: tuple[int, int]

def parse_instr(line: str) -> InstructionLine:
    def parse_range(rstr: str) -> tuple[int, int]:
        from_str, to_str = rstr[2:].split("..")
        # make second index excluding, as usual for ranges
        return int(from_str), int(to_str) + 1
    on_off, d = line.split()
    return InstructionLine(on_off == "on", *list(map(parse_range, d.split(",")))) # type: ignore


SAMPLE = len(argv) < 2 or argv[1] != "real"
instructions = read_lines(input_for(__file__, SAMPLE), parse_instr)

print("Collecting boundaries")
boundaries_x = sorted({c for instr in instructions for c in instr.rangex})
boundaries_y = sorted({c for instr in instructions for c in instr.rangey})
boundaries_z = sorted({c for instr in instructions for c in instr.rangez})

# this optimization allows quick access to a given boundary index
# given a coordinate, otherwise we'd need to search though the list of
# boundary indices
boundary_index_by_x = {x: i for i, x in enumerate(boundaries_x)}
boundary_index_by_y = {y: i for i, y in enumerate(boundaries_y)}
boundary_index_by_z = {z: i for i, z in enumerate(boundaries_z)}

# generate a 3d list of bools indicating the on/off state of a whole region
# according to the actual x, y, z coords determined in the sorted boundaries
# (maybe list comprehension would be faster?)
print("Creating multi-dim array for state...")
region_state: list[list[list[bool]]] = []
lengthx = len(boundaries_x)
for i in range(lengthx):
    print(f"{i} ouf of {lengthx}")
    region_state.append([[False for _ in boundaries_z] for _ in boundaries_y])


def boundary_range_for(coord_range: tuple[int, int], boundary_index_by_d: dict[int, int]) -> range:
    """
    Returns the range of boundary indices to interate over for a given range of coordinates
    """
    start, end = coord_range
    return range(boundary_index_by_d[start], boundary_index_by_d[end])

print("Applying on-off state from instructions...")
for i, instr in enumerate(instructions):
    print(f"{i} ouf of {len(instructions)}")
    for x in boundary_range_for(instr.rangex, boundary_index_by_x):
        for y in boundary_range_for(instr.rangey, boundary_index_by_y):
            for z in boundary_range_for(instr.rangez, boundary_index_by_z):
                region_state[x][y][z] = instr.on

print("Counting all regions...")
num = 0
lengthx = len(region_state)
for x in range(lengthx):
    print(f"{x} ouf of {lengthx}")
    for y in range(len(region_state[x])):
        for z in range(len(region_state[x][y])):
            if region_state[x][y][z]:
                num += (
                    (boundaries_x[x + 1] - boundaries_x[x])
                    * (boundaries_y[y + 1] - boundaries_y[y])
                    * (boundaries_z[z + 1] - boundaries_z[z])
                )

print_result(num)
