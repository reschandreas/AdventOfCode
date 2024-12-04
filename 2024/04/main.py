import re
from typing import List, Optional


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def first_part():
    matrix: List[List[str]] = []
    found: List[List[str]] = []
    for line in lines_of_file("first.txt"):
        matrix.append([c for c in line])
    for row in matrix:
        found.append(['.' for _ in row])
    found_xmas: int = 0
    for row, line in enumerate(matrix):
        for column, char in enumerate(line):
            if char == "X":
                down: List[str] = []
                down_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if row + i < len(matrix):
                            down_indizes.append((row + i, column))
                            down.append(matrix[row + i][column])
                except IndexError:
                    pass
                up: List[str] = []
                up_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if row - i >= 0:
                            up_indizes.append((row - i, column))
                            up.append(matrix[row - i][column])
                except IndexError:
                    pass
                diagonal_left_up: List[str] = []
                diagonal_left_up_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if row - i >= 0 and column - i >= 0:
                            diagonal_left_up_indizes.append((row - i, column - i))
                            diagonal_left_up.append(matrix[row - i][column - i])
                except IndexError:
                    pass
                diagonal_left_down: List[str] = []
                diagonal_left_down_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if row + i < len(matrix) and column - i >= 0:
                            diagonal_left_down_indizes.append((row + i, column - i))
                            diagonal_left_down.append(matrix[row + i][column - i])
                except IndexError:
                    pass
                diagonal_right_up: List[str] = []
                diagonal_right_up_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if row - i >= 0 and column + i <= len(line):
                            diagonal_right_up_indizes.append((row - i, column + i))
                            diagonal_right_up.append(matrix[row - i][column + i])
                except IndexError:
                    pass
                diagonal_right_down: List[str] = []
                diagonal_right_down_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if row + i <= len(matrix) and column + i <= len(line):
                            diagonal_right_down_indizes.append((row + i, column + i))
                            diagonal_right_down.append(matrix[row + i][column + i])
                except IndexError:
                    pass
                normal: List[str] = []
                normal_indizes: List[(int, int)] = []
                try:
                    normal = line[column:column + 4]
                    normal_indizes.append((row, column))
                    normal_indizes.append((row, column + 1))
                    normal_indizes.append((row, column + 2))
                    normal_indizes.append((row, column + 3))
                except IndexError:
                    pass
                backwards: List[str] = []
                backwards_indizes: List[(int, int)] = []
                try:
                    for i in [0, 1, 2, 3]:
                        if column - i >= 0:
                            backwards.append(line[column - i])
                            backwards_indizes.append((row, column - i))
                except IndexError:
                    pass

                for (c, indizes) in [
                    (normal, normal_indizes),
                    (backwards, backwards_indizes),
                    (up, up_indizes),
                    (down, down_indizes),
                    (diagonal_left_up, diagonal_left_up_indizes),
                    (diagonal_left_down, diagonal_left_down_indizes),
                    (diagonal_right_up, diagonal_right_up_indizes),
                    (diagonal_right_down,
                     diagonal_right_down_indizes)
                ]:
                    if len(c) != 4:
                        continue
                    haystack: str = ''.join(c)
                    if haystack in ["XMAS", "SAMX"]:
                        found_xmas += 1
                        for i, letter in enumerate(c):
                            x = indizes[i][0]
                            y = indizes[i][1]
                            found[x][y] = letter
    # for line in found:
    #     print(''.join(line))
    print(found_xmas)

def second_part():
    matrix: List[List[str]] = []
    found: List[List[str]] = []
    for line in lines_of_file("first.txt"):
        matrix.append([c for c in line])
    for row in matrix:
        found.append(['.' for _ in row])
    found_xmas: int = 0
    for row, line in enumerate(matrix):
        for column, char in enumerate(line):
            if char == "A":
                diagonal_left_up: List[str] = []
                diagonal_left_up_indizes: List[(int, int)] = []
                try:
                    for i in [-1, 0, 1]:
                        if row - i >= 0 and column - i >= 0:
                            diagonal_left_up_indizes.append((row - i, column - i))
                            diagonal_left_up.append(matrix[row - i][column - i])
                except IndexError:
                    pass
                diagonal_right_up: List[str] = []
                diagonal_right_up_indizes: List[(int, int)] = []
                try:
                    for i in [-1, 0, 1]:
                        if row - i >= 0 and column + i <= len(line):
                            diagonal_right_up_indizes.append((row - i, column + i))
                            diagonal_right_up.append(matrix[row - i][column + i])
                except IndexError:
                    pass
                found_x = 0
                matches: list = []
                for (c, indizes) in [
                    (diagonal_left_up, diagonal_left_up_indizes),
                    (diagonal_right_up, diagonal_right_up_indizes),
                ]:
                    if len(c) != 3:
                        continue
                    haystack: str = ''.join(c)
                    if haystack in ["MAS", "SAM"]:
                        matches.append((c, indizes))

                if len(matches) == 2:
                    for (c, indizes) in matches:
                        for i, letter in enumerate(c):
                            x = indizes[i][0]
                            y = indizes[i][1]
                            found[x][y] = letter
                    found_xmas += 1
    # for line in found:
    #     print(''.join(line))
    print(found_xmas)

def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
