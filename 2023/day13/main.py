"""
https://stackoverflow.com/a/56185125
"""
import os
import sys

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.



def transpose(toberows: [str]) -> [str]:
    lines = []
    length = len(toberows)
    size = len(toberows[0])
    for i in range(size):
        line = []
        for j in range(length):
            line.append(toberows[j][i])
        lines.append("".join(line))
    return lines


def find_mirror_second(lines: [str]) -> int | None:
    last = ""
    possibilities = []
    for i, line in enumerate(lines):
        if last == line:
            possibilities.append(i)
        last = line
    for p in possibilities:
        left = p
        side_a = lines[:left]
        side_a.reverse()
        side_b = lines[left:]
        one_plus = lines[left + 1]
        min_length = min(len(side_a), len(side_b))
        side_a = side_a[:min_length]
        side_b = side_b[:min_length]
        for i in range(min_length):
            tmp_a = side_a[:i]
            tmp_b = side_b[:i]
            if tmp_a == tmp_b:
                continue
            else:
                print("idk")
        if side_a != side_b:
            continue
        return left
    return None

def find_mirror_first(lines: [str]) -> int | None:
    last = ""
    possibilities = []
    for i, line in enumerate(lines):
        if last == line:
            possibilities.append(i)
        last = line
    for p in possibilities:
        left = p
        side_a = lines[:left]
        side_a.reverse()
        side_b = lines[left:]
        min_length = min(len(side_a), len(side_b))
        side_a = side_a[:min_length]
        side_b = side_b[:min_length]
        if side_a != side_b:
            continue
        return left
    return None

def find_value_of_pattern(pattern: str, method) -> int:
    lines = pattern.splitlines()
    columns = transpose(lines)
    mirror = method(columns)
    if mirror is None:
        mirr = method(lines)
        mirror = mirr * 100
    return mirror

def first():
    value: str = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    value = open("first.txt").read()
    patterns = value.split("\n\n")
    sum = 0
    for pattern in patterns:
        sum += find_value_of_pattern(pattern, find_mirror_first)
    print(sum)



def second():
    value: str = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

....##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    # value = open("first.txt").read()
    patterns = value.split("\n\n")
    sum = 0
    for pattern in patterns:
        sum += find_value_of_pattern(pattern, find_mirror_second)
    print(sum)


if __name__ == '__main__':
    first()
    #second()
