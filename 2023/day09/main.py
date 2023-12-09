"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
import math

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.
import re

def parse_line(line: str) -> [int]:
    return [int(i) for i in line.split(" ")]


def get_sequences(parsed):
    sequences: [[int]] = []
    for line in parsed:

        line_sequences = [line]
        all_zero = False
        while not all_zero:
            all_zero = True
            sequence = []
            for prev, current in zip(line_sequences[-1], line_sequences[-1][1:]):
                if current < 0 or prev < 0:
                    current = current
                tmp = current - prev
                if tmp != 0:
                    all_zero = False
                sequence.append(tmp)
            line_sequences.append(sequence)

        sequences.append(line_sequences)
    return sequences

def first():
    value: str = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    # value = open("first.txt", "r").read()
    lines = value.splitlines()
    parsed: [[int]] = [parse_line(line) for line in lines]

    new_lasts = []
    sequences = get_sequences(parsed)
    for sequence in sequences:
        lasts = [l[-1] for l in sequence]
        new_lasts.append(sum(lasts))
    print(sum(new_lasts))


def second():
    value: str = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    value = open("first.txt", "r").read()
    lines = value.splitlines()
    parsed: [[int]] = [parse_line(line) for line in lines]

    new_firsts = []
    sequences = get_sequences(parsed)
    for i, sequence in enumerate(sequences):
        for j, line in enumerate(sequence):
            sequences[i][j] = [0] + line
    for i, sequence in enumerate(sequences):
        for j, line in enumerate(reversed(sequence)):
            if j == len(sequence) - 1:
                continue
            current_index = len(sequence) - j - 1
            current_line = sequences[i][current_index]
            new_first = sequences[i][current_index - 1][1] - current_line[0]
            sequences[i][current_index - 1][0] = new_first
    for sequence in sequences:
        firsts = [l[0] for l in sequence]
        new_firsts.append(firsts[0])
    print(sum(new_firsts))



if __name__ == '__main__':
    #first()
    second()
