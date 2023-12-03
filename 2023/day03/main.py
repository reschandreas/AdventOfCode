"""
https://stackoverflow.com/a/56185125
"""
import os
import sys

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.
import utils


def get_number_at(marker: int, number_ranges: list[list[int]], haystack: str) -> int:
    for ran in number_ranges:
        if marker in ran:
            number: str = haystack[ran[0]: ran[-1] + 1]
            number = number
            return number


def get_number_ranges(indizes: list[int]) -> list[list[int]]:
    number_ranges: list[list[int]] = []
    last_row: list[int] = []
    for digit in indizes:
        if len(last_row) == 0:
            last_row.append(digit)
            continue
        if digit == last_row[-1] + 1:
            last_row.append(digit)
        else:
            number_ranges.append(last_row)
            last_row = [digit]
    if last_row:
        number_ranges.append(last_row)
    return number_ranges


def extract_numbers(indizes: list[int], markers: list[int], haystack: str) -> list[int]:
    numbers: list[int] = []
    ranges = get_number_ranges(indizes)
    for m in markers:
        number = get_number_at(marker=m, number_ranges=ranges, haystack=haystack)
        numbers.append(int(number))
    return numbers

def possible_gear(gearloc: int, indizes: list[int], markers: list[int], haystack: str) -> list[int]:
    numbers: list[int] = []
    ranges = get_number_ranges(indizes)
    for r in ranges:
        if gearloc in r:
            number = get_number_at(marker=gearloc, number_ranges=ranges, haystack=haystack)
            numbers.append(int(number))
    return numbers


def first():
    value: str = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    overall: int = 0
    prev_symbol_indexes: list[int] = []
    prev_number_indexes: list[int] = []
    prev_code: list[int] = []
    for line in utils.lines_of_file('first.txt'):
    # for line in utils.get_lines(value):
        code: list[int] = []
        l: str = line
        for c in l:
            if c.isdigit():
                code.append(c)
            elif c == '.':
                code.append('d')
            else:
                code.append('s')
        number_indexes = [i for i, x in enumerate(code) if x.isdigit()]
        symbol_indexes = [i for i, x in enumerate(code) if x == 's']
        direct_up: list[int] = [s for s in symbol_indexes if s in prev_number_indexes]
        direct_down: list[int] = [s for s in prev_symbol_indexes if s in number_indexes]
        direct_back: list[int] = [s - 1 for s in symbol_indexes if s - 1 in number_indexes]
        direct_front: list[int] = [s + 1 for s in symbol_indexes if s + 1 in number_indexes]
        adjacent_up_back: list[int] = [s - 1 for s in symbol_indexes if s - 1 in prev_number_indexes and s not in direct_up]
        adjacent_up_front: list[int] = [s + 1 for s in symbol_indexes if s + 1 in prev_number_indexes and s not in direct_up]
        adjacent_down_back: list[int] = [s - 1 for s in prev_symbol_indexes if s - 1 in number_indexes and s not in direct_down]
        adjacent_down_front: list[int] = [s + 1 for s in prev_symbol_indexes if s + 1 in number_indexes and s not in direct_down]
        already_counted_prev_line: list[int] = []
        already_counted_this_line: list[int] = []
        if direct_up:
            numbers = extract_numbers(
                markers=direct_up, indizes=prev_number_indexes, haystack="".join(prev_code)
            )
            # numbers = [x for x in numbers if x not in already_counted_prev_line]
            already_counted_prev_line += numbers
            print("direct, up", numbers)
            already_counted_this_line += numbers
            overall += sum(numbers)
        if direct_down:
            numbers = extract_numbers(
                markers=direct_down, indizes=number_indexes, haystack="".join(code)
            )
            # numbers = [x for x in numbers if x not in already_counted_prev_line]
            already_counted_prev_line += numbers
            print("direct, down", numbers)
            already_counted_this_line += numbers
            overall += sum(numbers)
        if adjacent_up_back:
            numbers = extract_numbers(
                markers=adjacent_up_back, indizes=prev_number_indexes, haystack="".join(prev_code)
                )
            # numbers = [x for x in numbers if x not in already_counted_prev_line]
            already_counted_prev_line += numbers
            print("up, back", numbers)
            already_counted_this_line += numbers
            overall += sum(numbers)
        if adjacent_up_front:
            numbers = extract_numbers(
                markers=adjacent_up_front, indizes=prev_number_indexes, haystack="".join(prev_code)
                )
            # numbers = [x for x in numbers if x not in already_counted_prev_line]
            already_counted_prev_line += numbers
            print("up, front", numbers)
            overall += sum(numbers)
        if adjacent_down_back:
            numbers = extract_numbers(markers=adjacent_down_back, indizes=number_indexes, haystack="".join(code))
            # numbers = [x for x in numbers if x not in already_counted_this_line]
            already_counted_this_line += numbers
            print("down, back", numbers)
            overall += sum(numbers)
        if adjacent_down_front:
            numbers = extract_numbers(markers=adjacent_down_front, indizes=number_indexes, haystack="".join(code))
            # numbers = [x for x in numbers if x not in already_counted_this_line]
            print("down, front", numbers)
            already_counted_this_line += numbers
            overall += sum(numbers)
        if direct_back:
            numbers = extract_numbers(markers=direct_back, indizes=number_indexes, haystack="".join(code))
            # numbers = [x for x in numbers if x not in already_counted_this_line]
            already_counted_this_line += numbers
            print("direct, back", numbers)
            overall += sum(numbers)
        if direct_front:
            numbers = extract_numbers(markers=direct_front, indizes=number_indexes, haystack="".join(code))
            print("direct, front", numbers)
            already_counted_this_line += numbers
            overall += sum(numbers)
        print('found this line', already_counted_this_line)
        prev_code = code
        prev_number_indexes = number_indexes
        prev_symbol_indexes = symbol_indexes
    print(overall)


def second():
    value: str = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    overall: int = 0
    prev_symbol_indexes: list[int] = []
    prev_number_indexes: list[int] = []
    prev_code: list[int] = []
    gear_candidates: list[(int, int, int)] = []
    line_number: int = 0
    for line in utils.lines_of_file('second.txt'):
    # for line in utils.get_lines(value):
        line_number += 1
        code: list[int] = []
        l: str = line
        for c in l:
            if c.isdigit():
                code.append(c)
            elif c != '*':
                code.append('d')
            else:
                code.append('s')
        number_indexes = [i for i, x in enumerate(code) if x.isdigit()]
        symbol_indexes = [i for i, x in enumerate(code) if x == 's']
        direct_up: list[int] = [s for s in symbol_indexes if s in prev_number_indexes]
        direct_down: list[int] = [s for s in prev_symbol_indexes if s in number_indexes]
        direct_back: list[int] = [s - 1 for s in symbol_indexes if s - 1 in number_indexes]
        direct_front: list[int] = [s + 1 for s in symbol_indexes if s + 1 in number_indexes]
        adjacent_up_back: list[int] = [s - 1 for s in symbol_indexes if
                                       s - 1 in prev_number_indexes and s not in direct_up]
        adjacent_up_front: list[int] = [s + 1 for s in symbol_indexes if
                                        s + 1 in prev_number_indexes and s not in direct_up]
        adjacent_down_back: list[int] = [s - 1 for s in prev_symbol_indexes if
                                         s - 1 in number_indexes and s not in direct_down]
        adjacent_down_front: list[int] = [s + 1 for s in prev_symbol_indexes if
                                          s + 1 in number_indexes and s not in direct_down]
        if direct_up:
            for m in symbol_indexes:
                possible = possible_gear(gearloc=m, indizes=prev_number_indexes, haystack="".join(prev_code), markers=direct_up)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if direct_down:
            for m in prev_symbol_indexes:
                possible = possible_gear(gearloc=m, indizes=number_indexes, haystack="".join(code), markers=direct_down)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if adjacent_up_back:
            for m in symbol_indexes:
                possible = possible_gear(gearloc=m - 1, indizes=prev_number_indexes, haystack="".join(prev_code), markers=adjacent_up_back)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if adjacent_up_front:
            for m in symbol_indexes:
                possible = possible_gear(gearloc=m + 1, indizes=prev_number_indexes, haystack="".join(prev_code), markers=adjacent_up_front)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if adjacent_down_back:
            for m in prev_symbol_indexes:
                possible = possible_gear(gearloc=m - 1, indizes=number_indexes, haystack="".join(code), markers=adjacent_down_back)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if adjacent_down_front:
            for m in prev_symbol_indexes:
                possible = possible_gear(gearloc=m + 1, indizes=number_indexes, haystack="".join(code), markers=adjacent_down_front)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if direct_back:
            for m in symbol_indexes:
                possible = possible_gear(gearloc=m - 1, indizes=number_indexes, haystack="".join(code), markers=direct_back)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        if direct_front:
            for m in symbol_indexes:
                possible = possible_gear(gearloc=m + 1, indizes=number_indexes, haystack="".join(code), markers=direct_front)
                if possible:
                    gear_candidates.append((possible[0], m, line_number))
        prev_code = code
        prev_number_indexes = number_indexes
        prev_symbol_indexes = symbol_indexes
        line_number += 1
    print(gear_candidates)
    product: int = 0
    locked = []
    for candidate in gear_candidates:
        number, index, line = candidate
        if candidate in locked:
            continue
        for second in gear_candidates:
            if second in locked:
                continue
            if candidate != second:
                number_second, index_second, line_second = second
                if index_second == index:
                    if line_second in range(line, line + 3):
                        product += number * number_second
                        locked.append(second)
                        locked.append(candidate)
    print(product)


if __name__ == '__main__':
    #first()
    second()
