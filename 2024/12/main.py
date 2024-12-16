from typing import List, Dict, Tuple, Set


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_input() -> List[List[str]]:
    matrix: List[List[str]] = []
    for line in lines_of_file("first.txt"):
        matrix.append([c for c in line])
    return matrix


def count_borders(position: Tuple[int, int], plant: str, matrix: List[List[str]]) -> int:
    tmp = get_all_neighbors(position=position, matrix=matrix, diagonal=False)
    return 4 - len([c for _, _, c in tmp if c == plant])


def get_borders(position: Tuple[int, int], matrix: List[List[str]]) -> set[tuple[int, int, str]]:
    return get_all_neighbors(position=position, matrix=matrix, diagonal=False)


def print_matrix(matrix: List[List[str]]):
    for line in matrix:
        line = "".join(line)
        if line.strip():
            print(line)


def get_all_neighbors(position: Tuple[int, int], matrix: List[List[str]], diagonal: bool = True) -> Set[
    Tuple[int, int, str]]:
    row, col = position
    neighbors: Set[Tuple[int, int, str]] = set()
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if not diagonal:
                if (x, y) in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
                    continue
            if x == 0 and y == 0:
                continue
            if row + x < 0 or col + y < 0:
                continue
            if row + x >= len(matrix) or col + y >= len(matrix[row + x]):
                continue
            try:
                neighbors.add((row + x, col + y, matrix[row + x][col + y]))
            except IndexError as _:
                pass
    return neighbors


def find_all_neighbors(char: str, position: Tuple[int, int], matrix: List[List[str]]) -> List[Tuple[int, int]]:
    area: Set[Tuple[int, int]] = set()
    area.add(position)
    working_set: Set[Tuple[int, int]] = set()
    working_set.add(position)
    looked_at: Set[Tuple[int, int, str]] = set()
    while len(working_set) > 0:
        candidate: Tuple[int, int] = working_set.pop()
        all_neighbors = get_all_neighbors(position=candidate, matrix=matrix, diagonal=False)
        for neighbor in all_neighbors - looked_at:
            x, y, value = neighbor
            looked_at.add(neighbor)
            if value == char:
                if (x, y) not in area:
                    working_set.add((x, y))
                area.add((x, y))
    return list(area)


def first_part():
    matrix: List[List[str]] = get_input()
    areas: Dict[str, List[List[Tuple[int, int]]]] = {}
    already_mapped: Set[Tuple[int, int]] = set()
    for row, line in enumerate(matrix):
        for column, cell in enumerate(line):
            if (row, column) in already_mapped:
                continue
            area: List[Tuple[int, int]] = find_all_neighbors(char=cell, position=(row, column), matrix=matrix)
            for a in area:
                already_mapped.add(a)
            if cell not in areas:
                areas[cell] = []
            areas[cell].append(area)
    # fences: List[List[str]] = []
    # for i in range(len(matrix) + 2):
    #     tmp = []
    #     for i in range(len(matrix[0]) + 2):
    #         tmp.append(' ')
    #     fences.append(tmp)
    price: int = 0
    for char in areas:
        for area in areas[char]:
            room: int = 0
            borders: int = 0
            # outers: int = 0
            # b: Set[Tuple[int, int]] = set()
            fences: List[List[str]] = []
            for i in range(len(matrix) + 2):
                tmp = []
                for i in range(len(matrix[0]) + 2):
                    tmp.append(' ')
                fences.append(tmp)
            for cell in area:
                room += 1
                borders += count_borders(position=cell, plant=char, matrix=matrix)
                # for (x, y, t) in get_borders(position=cell, matrix=matrix):
                #     if t == char:
                #         continue
                #     b.add((x, y))
                #     fences[x + 1][y + 1] = '+'
                # if row == 0:
                #     # b.add((-1, col))
                #     fences[row][col + 1] = '+'
                # if col == 0:
                #     # b.add((row, -1))
                #     fences[row + 1][col] = '+'
                # if row >= len(matrix) - 1:
                #     # b.add((row + 1, col))
                #     fences[row + 2][col + 1] = '+'
                # if col >= len(matrix[row]) - 1:
                #     # b.add((row, col + 1))
                #     fences[row + 1][col + 2] = '+'
            # print_matrix(matrix=fences)
            price += room * borders
    # for char in areas:
    #     print(char, len(areas[char]))
    print("price", price)


def transpose(matrix: List[List[str]]) -> List[List[str]]:
    transposed: List[List[str]] = []
    for col in range(len(matrix[0])):
        new_row: List[str] = []
        for row in range(len(matrix)):
            new_row.append(matrix[row][col])
        transposed.append(new_row)
    return transposed


def count_sides(matrix: List[List[str]]) -> Tuple[int, int]:
    horizontal: int = 0
    vertical: int = 0
    for line in matrix:
        strings: str = "".join(line).replace('|', ' ').strip()
        counter: List[str] = [s for s in strings.split(" ") if s and not s.isalpha()]
        horizontal += len(counter)
    transposed = transpose(matrix=matrix)
    for line in transposed:
        strings: str = "".join(line).replace('-', ' ').strip()
        counter: List[str] = [s for s in strings.split(" ") if s and not s.isalpha()]
        vertical += len(counter)
    return horizontal, vertical


def second_part():
    matrix: List[List[str]] = get_input()
    areas: Dict[str, List[List[Tuple[int, int]]]] = {}
    already_mapped: Set[Tuple[int, int]] = set()
    for row, line in enumerate(matrix):
        for column, cell in enumerate(line):
            if (row, column) in already_mapped:
                continue
            area: List[Tuple[int, int]] = find_all_neighbors(char=cell, position=(row, column), matrix=matrix)
            for a in area:
                already_mapped.add(a)
            if cell not in areas:
                areas[cell] = []
            areas[cell].append(area)
    price: int = 0
    multiplier: int = 3
    for char in areas:
        for area in areas[char]:
            room: int = 0
            b: Set[Tuple[int, int]] = set()
            fences: List[List[str]] = []
            for i in range(len(matrix) * multiplier):
                tmp = []
                for i in range(len(matrix[0]) * multiplier):
                    tmp.append(' ')
                fences.append(tmp)
            for cell in area:
                room += 1
                row, col = cell
                r_offset: int = 1 if row == 0 else 0
                c_offset: int = 1 if col == 0 else 0
                fences[multiplier * row + r_offset][multiplier * col + c_offset] = char
                for (x, y, t) in get_borders(position=cell, matrix=matrix):
                    if t == char:
                        continue
                    b.add((x, y))
                    side: str = '-' if x in [row + 1, row - 1] else '|'

                    diff_x: int = x - row + (1 if row == 0 else 0)
                    diff_y: int = y - col + (1 if col == 0 else 0)

                    if fences[multiplier * row + diff_x][multiplier * col + diff_y] in ['-', '|'] and side != fences[multiplier * row + diff_x][
                        multiplier * diff_y + diff_y]:
                        side = '+'
                    if multiplier * row + diff_x >= 0 and multiplier * col + diff_y >= 0:
                        fences[multiplier * row + diff_x][multiplier * col + diff_y] = side
                        if side == '-':
                            fences[multiplier * row + diff_x][multiplier * col + diff_y - 1] = side
                            fences[multiplier * row + diff_x][multiplier * col + diff_y + 1] = side
                        else:
                            fences[multiplier * row + diff_x - 1][multiplier * col + diff_y] = side
                            fences[multiplier * row + diff_x + 1][multiplier * col + diff_y] = side
                if row == 0:
                    fences[row][multiplier * col + c_offset] = '-'
                    fences[row][multiplier * col + c_offset - 1] = '-'
                    fences[row][multiplier * col + c_offset + 1] = '-'
                if col == 0:
                    fences[multiplier * row + r_offset - 1][col] = '|'
                    fences[multiplier * row + r_offset][col] = '|'
                    fences[multiplier * row + r_offset + 1][col] = '|'
                if row >= len(matrix) - 1:
                    fences[multiplier * row + 1][multiplier * col + c_offset - 1] = '-'
                    fences[multiplier * row + 1][multiplier * col + c_offset] = '-'
                    fences[multiplier * row + 1][multiplier * col + c_offset + 1] = '-'
                if col >= len(matrix[row]) - 1:
                    fences[multiplier * row + r_offset - 1][multiplier * col + 1] = '|'
                    fences[multiplier * row + r_offset][multiplier * col + 1] = '|'
                    fences[multiplier * row + r_offset + 1][multiplier * col + 1] = '|'
            # print_matrix(matrix=fences)
            horizontal, vertical = count_sides(matrix=fences)
            sides: int = horizontal + vertical
            # print(char, room, sides)
            price += room * sides
    print("price", price)


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
