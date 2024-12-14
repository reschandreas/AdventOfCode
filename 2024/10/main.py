from typing import List, Tuple, Optional, Set, Dict


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_input() -> List[List[int]]:
    matrix: List[List[int]] = []
    for line in lines_of_file("first.txt"):
        matrix.append([int(c) if c != '.' else -1 for c in line])
    return matrix


def get_starting_positions(matrix: List[List[int]]) -> List[Tuple[int, int]]:
    points: List[Tuple[int, int]] = []
    for row, line in enumerate(matrix):
        for column, cell in enumerate(line):
            if cell == 0:
                points.append((row, column))
    return points


def get_next_steps(matrix: List[List[int]], position: Tuple[int, int], height: int) -> List[Tuple[int, int]]:
    x, y = position
    up: Optional[Tuple[int, int]] = None
    down: Optional[Tuple[int, int]] = None
    left: Optional[Tuple[int, int]] = None
    right: Optional[Tuple[int, int]] = None
    next_steps: List[Tuple[int, int]] = []
    if x > 0:
        up = (x - 1, y)
    if x < len(matrix) - 1:
        down = (x + 1, y)
    if y > 0:
        left = (x, y - 1)
    if y < len(matrix[x]) - 1:
        right = (x, y + 1)
    if up and matrix[up[0]][up[1]] == height + 1:
        next_steps.append(up)
    if down and matrix[down[0]][down[1]] == height + 1:
        next_steps.append(down)
    if left and matrix[left[0]][left[1]] == height + 1:
        next_steps.append(left)
    if right and matrix[right[0]][right[1]] == height + 1:
        next_steps.append(right)
    return next_steps


def first_part():
    matrix: List[List[int]] = get_input()
    starting_positions: List[Tuple[int, int]] = get_starting_positions(matrix=matrix)
    paths: List[List[Tuple[int, int, int]]] = []
    counter: Dict[Tuple[int, int], Set[Tuple[int, int]]] = {}
    working_set: List[List[Tuple[int, int, int]]] = []
    for position in starting_positions:
        x, y = position
        paths.append([(x, y, 0)])
        working_set.append([(x, y, 0)])
        counter[(x, y)] = set()
    while len(working_set) > 0:
        path = working_set.pop()
        x, y, height = path[-1]
        next_ones = get_next_steps(matrix=matrix, position=(x, y), height=height)
        for next in next_ones:
            x, y = next
            tmp = path.copy()
            tmp.append((x, y, height + 1))
            if height + 1 < 9:
                working_set.append(tmp)
            else:
                counter[(path[0][0], path[0][1])].add((x, y))

    trails: int = sum([len(counter[(x, y)]) for x, y in starting_positions])
    print("trails", trails)


def second_part():
    matrix: List[List[int]] = get_input()
    starting_positions: List[Tuple[int, int]] = get_starting_positions(matrix=matrix)
    paths: List[List[Tuple[int, int, int]]] = []
    counter: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = {}
    working_set: List[List[Tuple[int, int, int]]] = []
    for position in starting_positions:
        x, y = position
        paths.append([(x, y, 0)])
        working_set.append([(x, y, 0)])
        counter[(x, y)] = []
    while len(working_set) > 0:
        path = working_set.pop()
        x, y, height = path[-1]
        next_ones = get_next_steps(matrix=matrix, position=(x, y), height=height)
        for next in next_ones:
            x, y = next
            tmp = path.copy()
            tmp.append((x, y, height + 1))
            if height + 1 < 9:
                working_set.append(tmp)
            else:
                counter[(path[0][0], path[0][1])].append(tmp)

    trails: int = sum([len(counter[(x, y)]) for x, y in starting_positions])
    print("trails", trails)


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
