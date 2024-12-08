import itertools
from typing import List, Dict, Any


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_input() -> List[List[str]]:
    matrix: List[List[str]] = []
    for line in lines_of_file('first.txt'):
        matrix.append([c for c in line])
    return matrix

def print_matrix(matrix: List[List[str]]):
    for line in matrix:
        print("".join(line))


def collect_antennas(matrix: List[List[str]]) -> dict[str, list[(int, int)]]:
    antennas: dict[str, List[(int, int)]] = {}
    for row, line in enumerate(matrix):
        for columm, char in enumerate(line):
            if char == '.' and char != '#':
                continue
            if not char in antennas:
                antennas[char] = []
            antennas[char].append((row, columm))
    return antennas


def compute_antinodes(antennas: List[Any]) -> List[Any]:
    antinodes: set = set()
    for p in itertools.combinations(antennas, 2):
        first, second = p
        fx, fy = first
        sx, sy = second
        diff_x = fx - sx
        diff_y = fy - sy
        antinodes.add((fx - 2 * diff_x, fy - 2 * diff_y))
        # antinodes.add((fx + 2 * diff_x, fy + 2 * diff_y))
        antinodes.add((sx + 2 * diff_x, sy + 2 * diff_y))
    return [(a, b) for (a, b) in list(antinodes) if a >= 0 and b >= 0]
    # return list(antinodes - set(antennas))


def first_part():
    matrix: List[List[str]] = get_input()
    all_antennas = set()
    antennas = collect_antennas(matrix=matrix)
    antinodes = []
    closer_look: str = '4'
    for antenna in antennas:
        # if antenna != closer_look:
        #     continue
        for a in antennas[antenna]:
            all_antennas.add(a)
        for antinode in compute_antinodes(antennas=antennas[antenna]):
            antinodes.append(antinode)

    for (x, y) in set(antinodes):
        if x < len(matrix):
            if y < len(matrix[x]):
                matrix[x][y] = '#'
    print("all in all", len(set([(x, y) for (x, y) in antinodes if 0 <= x < len(matrix) and 0 <= y < len(matrix[x])])))
    # print_matrix(matrix=matrix)

def second_part():
    pass


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
