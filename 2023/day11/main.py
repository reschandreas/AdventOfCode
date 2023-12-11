"""
https://stackoverflow.com/a/56185125
"""
import os
import sys

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.


def get_lines_working(string: str) -> [([int], str)]:
    lines = []
    # expand rows
    for line in string.splitlines():
        if '#' not in line:
            lines.append(line)
        lines.append(line)
    # expand columns
    columns = []
    for i in range(len(lines[0])):
        column = []
        for j in range(len(lines)):
            column.append(lines[j][i])
        columns.append(column)
    lines = []
    for column in columns:
        stri = "".join(column)
        if '#' not in stri:
            lines.append(stri)
        lines.append(stri)
    columns = []
    for i in range(len(lines[0])):
        column = []
        for j in range(len(lines)):
            column.append(lines[j][i])
        columns.append(column)
    new_lines = ["".join(c) for c in columns]
    lines = []
    for line in new_lines:
        if '#' not in line:
            lines.append((None, line))
        else:
            lines.append(([i for i, c in enumerate(line) if c == '#'], line))
    return lines


def get_lines(string: str, spacer: int) -> [([int], str)]:
    lines = []
    # expand rows
    line_indices = []
    line_index = 0
    for i, line in enumerate(string.splitlines()):
        if '#' not in line:
            line_index += spacer
        else:
            line_index += 1
        line_indices.append(line_index)
        lines.append(line)
    # expand columns
    columns = []
    for i in range(len(lines[0])):
        column = []
        for j in range(len(lines)):
            char = lines[j][i]
            column.append(char)
        columns.append(column)
    lines = []
    for column in columns:
        stri = "".join(column)
        lines.append(stri)
    columns = []
    for i in range(len(lines[0])):
        column = []
        for j in range(len(lines)):
            column.append(lines[j][i])
        columns.append(column)
    rows = []
    for i in range(len(columns)):
        row = []
        for j in range(len(columns[0])):
            char = columns[j][i]
            row.append(char)
        rows.append(row)
    columns_changed = ["".join(c) for c in rows]
    column_index = 0
    column_indices = []
    for i, line in enumerate(columns_changed):
        if '#' not in line:
            column_index += spacer
        else:
            column_index += 1
        column_indices.append(column_index)
    lines = []
    index = 0
    for line in string.splitlines():
        if '#' not in line:
            pass
        else:
            real_index = line_indices[index]
            galaxies = [column_indices[i] for i, c in enumerate(line) if c == '#']
            lines.append((real_index, galaxies, line))
        index += 1
    return lines


def shortest_path(a: (int, int), b: (int, int)) -> int:
    x_diff = max(a[0], b[0]) - min(a[0], b[0])
    y_diff = max(a[1], b[1]) - min(a[1], b[1])
    return x_diff + y_diff


def first():
    value: str = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    lines = get_lines(value, spacer=2)
    numbers = []
    for i, (real, indexes, l) in enumerate(lines):
        if indexes is None:
            numbers.append((real, i, []))
        else:
            numbers.append((real, i, indexes))
        print(l)
    paths: dict = {}
    for real, line, indexes in numbers:
        for index in indexes:
            candidates = [n for n in numbers if n[0] >= line]
            for c_real, c_line, c_index in candidates:
                for c_element in c_index:
                    if real == c_real and c_element <= index or c_real < real:
                        continue
                    paths[f"from-line-{real}-{index}-to-{c_real}-{c_element}"] = shortest_path(
                        (real, index), (c_real, c_element)
                        )
    print(sum(paths.values()))


def second():
    value: str = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    value = open("first.txt").read()
    lines = get_lines(value, spacer=1_000_000)
    numbers = []
    for i, (real, indexes, l) in enumerate(lines):
        if indexes is None:
            numbers.append((real, i, []))
        else:
            numbers.append((real, i, indexes))
        print(l)
    paths: dict = {}
    for real, line, indexes in numbers:
        for index in indexes:
            candidates = [n for n in numbers if n[0] >= line]
            for c_real, c_line, c_index in candidates:
                for c_element in c_index:
                    if real == c_real and c_element <= index or c_real < real:
                        continue
                    paths[f"from-line-{real}-{index}-to-{c_real}-{c_element}"] = shortest_path(
                        (real, index), (c_real, c_element)
                        )
    print(sum(paths.values()))


if __name__ == '__main__':
    first()
    second()
