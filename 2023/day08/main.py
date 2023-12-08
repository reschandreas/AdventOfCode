"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
import math
sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.


def parse_line(line: str):
    parts = line.split(" = (")
    point_a = parts[0]
    parts = parts[1].split(", ")
    point_b = parts[0]
    point_c = parts[1].replace(")", "")
    return point_a, point_b, point_c


def first():
    value: str = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    value: str = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    value = open("first.txt", "r").read()
    lines = value.splitlines()
    instructions = lines.pop(0)
    if lines[0] == '':
        lines.pop(0)
    parsed_line = {}
    order = []
    dead_ends = set()
    for line in lines:
        a, b, c = parse_line(line)
        order.append(a)
        if a == b and b == c:
            dead_ends.add(a)
            parsed_line[a] = ['dead', 'end']
        else:
            parsed_line[a] = [b, c]
    i = 0
    steps = 0
    current_location = "AAA"
    while current_location != "ZZZ":
        command = parsed_line[current_location]
        if instructions[i] == 'L':
            current_location = command[0]
        else:
            current_location = command[1]
        i += 1
        if i >= len(instructions):
            i = 0
        steps += 1
    print(steps)
    print(parsed_line)


def second():
    value: str = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    value = open("first.txt", "r").read()
    lines = value.splitlines()
    instructions = lines.pop(0)
    if lines[0] == '':
        lines.pop(0)
    parsed_line = {}
    order = []
    dead_ends = set()
    for line in lines:
        a, b, c = parse_line(line)
        order.append(a)
        if a == b and b == c:
            dead_ends.add(a)
        else:
            parsed_line[a] = [b, c]
    i = 0
    steps = 0
    # 21251 too low
    current_locations = [loc for loc in parsed_line.keys() if loc.endswith("A")]
    was_at_location = [0 for loc in parsed_line.keys() if loc.endswith("A")]

    i = 0
    while any([loc == 0 for loc in was_at_location]):
        steps += 1
        for index, location in enumerate(current_locations):
            command = parsed_line[location]
            if instructions[i] == 'L':
                current_locations[index] = command[0]
            else:
                current_locations[index] = command[1]

            if current_locations[index].endswith("Z"):
                was_at_location[index] = steps
        i += 1
        if i >= len(instructions):
            i = 0
    print(f"Overall {lcm(was_at_location)}")

def lcm(array: list) -> int:
    lcm = 1
    for i in array:
        lcm = lcm * i // math.gcd(lcm, i)
    return lcm


if __name__ == '__main__':
    # first()
    second()
