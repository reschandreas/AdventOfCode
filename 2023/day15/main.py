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

def hash_of_char(previous: int, char: str) -> int:
    return ((previous + ord(char)) * 17) % 256

def get_hash_of(current: int, value: str) -> int:
    for i in value:
        current = hash_of_char(current, i)
    return current

def first():
    value: str = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    value = open("first.txt").read()
    inputs = value.split(",")
    results = []
    current = 0
    for seq in inputs:
        current = get_hash_of(0, seq)
        results.append(current)
    print(sum(results))



def second():
    pass


if __name__ == '__main__':
    first()
