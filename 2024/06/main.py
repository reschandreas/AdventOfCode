from typing import List, Optional


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_next_sign(sign: str):
    if sign == '^':
        return '>'
    if sign == '>':
        return 'v'
    if sign == 'v':
        return '<'
    if sign == '<':
        return '^'
    return '.'


def get_next_cell_indizes(guard_position: (int, int, str)):
    row, column, direction = guard_position
    if direction == '^':
        row -= 1
    elif direction == '<':
        column -= 1
    elif direction == '>':
        column += 1
    elif direction == 'v':
        row += 1
    return row, column


def wall_ahead(guard_position: (int, int, str), matrix: List[List[str]]) -> Optional[bool]:
    (nrow, ncolumn) = get_next_cell_indizes(guard_position=guard_position)
    if is_outside(nrow, ncolumn, len(matrix)):
        return None
    return matrix[nrow][ncolumn] == '#'


def get_next_cell(guard_position: (int, int, str), matrix: List[List[str]]):
    (nrow, ncolumn) = get_next_cell_indizes(guard_position=guard_position)
    if is_outside(nrow, ncolumn, len(matrix)):
        return None
    return matrix[nrow][ncolumn]


def get_next(guard_position: (int, int, str), matrix: List[List[str]]):
    (ogr, ogc, direction) = guard_position
    wall = wall_ahead(guard_position=guard_position, matrix=matrix)
    if wall is None:
        return None
    if wall:  # turn once
        next_sign = get_next_sign(direction)
        row, column = get_next_cell_indizes(guard_position=(ogr, ogc, next_sign))
        return row, column, next_sign
    row, column = get_next_cell_indizes(guard_position=guard_position)
    return row, column, direction


def is_outside(row: int, column: int, length: int):
    return row < 0 or column < 0 or row >= length or column >= length


def find_loop(guard_position: (int, int, str), matrix: List[List[str]]):
    matrix_size = len(matrix)
    unique: set[((int, int), str)] = set()
    while True:
        row, column, direction = guard_position
        if is_outside(row, column, matrix_size):
            return False
        tmp = len(unique)
        unique.add(((row, column), direction))
        wall = wall_ahead(guard_position=guard_position, matrix=matrix)
        if wall is None:
            return False
        if wall:
            new_direction = get_next_sign(direction)
            guard_position = (row, column, new_direction)
        guard_position = get_next(guard_position=guard_position, matrix=matrix)
        if not guard_position:
            return False
        row, column, _ = guard_position
        if direction != guard_position[2]:
            if len(set(unique)) == tmp:
                return True


def brute_force(matrix: List[List[str]], guard_position: (int, int, str)):
    obstacles: int = 0
    for row, line in enumerate(matrix):
        for column, cell in enumerate(matrix):
            if cell == '#' or cell == '^':
                continue
            tmp = clone_matrix(matrix=matrix)
            tmp[row][column] = '#'
            if find_loop(guard_position=guard_position, matrix=tmp):
                matrix[row][column] = 'O'
                obstacles += 1
    # for line in matrix:
    #     print("".join(line))
    print("obstacles", obstacles)


def clone_matrix(matrix: List[List[str]]) -> List[List[str]]:
    tmp: List[List[str]] = []
    for line in matrix:
        tmp.append(line.copy())
    return tmp

def move_with_loop_check(guard_position: (int, int, str), matrix: List[List[str]]):
    out_of_map: bool = False
    matrix_size: int = len(matrix)
    visited_cells: set = set()
    start = guard_position
    unique_loops: set = set()
    while not out_of_map:
        row, column, direction = guard_position
        if is_outside(row, column, matrix_size):
            return True
        visited_cells.add((row, column))
        wall = wall_ahead(guard_position=guard_position, matrix=matrix)
        if wall is None:
            break
        if wall:
            new_direction = get_next_sign(direction)
            guard_position = (row, column, new_direction)
        next_cell = get_next_cell(guard_position=guard_position, matrix=matrix)
        if next_cell and next_cell != '#':
            tmp = clone_matrix(matrix=matrix)
            r, c = get_next_cell_indizes(guard_position=guard_position)
            tmp[r][c] = '#'
            if find_loop(guard_position=start, matrix=tmp):
                unique_loops.add((r, c))
        guard_position = get_next(guard_position=guard_position, matrix=matrix)
        if not guard_position:
            break
    return len(unique_loops)

def move(guard_position: (int, int, str), matrix: List[List[str]]):
    out_of_map: bool = False
    matrix_size: int = len(matrix)
    visited_cells: set = set()
    while not out_of_map:
        row, column, direction = guard_position
        if is_outside(row, column, matrix_size):
            return True
        visited_cells.add((row, column))
        wall = wall_ahead(guard_position=guard_position, matrix=matrix)
        if wall is None:
            break
        if wall:
            new_direction = get_next_sign(direction)
            guard_position = (row, column, new_direction)
        guard_position = get_next(guard_position=guard_position, matrix=matrix)
        if not guard_position:
            return len(visited_cells)
    return len(visited_cells)


def get_guard_position(matrix: List[List[str]]) -> (int, int, str):
    for row, line in enumerate(matrix):
        for column, cell in enumerate(line):
            if cell == '^':
                return row, column, '^'


def first_part():
    matrix: List[List[str]] = []
    for row, line in enumerate(lines_of_file("first.txt")):
        matrix.append([c for c in line])
    guard_position: Optional[(int, int, str)] = get_guard_position(matrix=matrix)
    steps: int = move(guard_position=guard_position, matrix=matrix)
    print(steps)
    # for line in matrix:
    #     print("".join(line))


def second_part():
    matrix: List[List[str]] = []
    for row, line in enumerate(lines_of_file("first.txt")):
        matrix.append([c for c in line])
    guard_position: Optional[(int, int, str)] = get_guard_position(matrix=matrix)
    # brute_force(guard_position=guard_position, matrix=matrix)
    loops: int = move_with_loop_check(guard_position=guard_position, matrix=matrix)
    print("loops", loops)


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
