import re
from typing import List, Tuple, Optional


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_input() -> List[str]:
    matrix: List[str] = []
    for line in lines_of_file("first.txt"):
        matrix.append(line)
    return matrix


def read_button_a(line: str) -> Tuple[int, int]:
    match = re.findall(r"\+(\d*)", line)
    return int(match[0]), int(match[1])


def read_button_b(line: str) -> Tuple[int, int]:
    match = re.findall(r"\+(\d*)", line)
    return int(match[0]), int(match[1])


def read_prize(line: str) -> Tuple[int, int]:
    match = re.findall(r"=(\d*)", line)
    return int(match[0]), int(match[1])


def get_machines() -> List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    lines: List[str] = get_input()
    tmp: List[List[str]] = []
    machine: List[str] = []
    for line in lines:
        if line.strip():
            machine.append(line)
        else:
            tmp.append(machine)
            machine = []
    tmp.append(machine)
    machines: List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]] = []
    for machine in tmp:
        button_a: Tuple[int, int] = read_button_a(machine[0])
        button_b: Tuple[int, int] = read_button_b(machine[1])
        prize: Tuple[int, int] = read_prize(machine[2])
        machines.append((button_a, button_b, prize))
    return machines


# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
#
# 94a + 22b = 8400
# 34a + 67b = 5400
#
# 34a = 5400 - 67b
# a = 5400/34 - 67b/34
#
# 94(5400/34 - 67b/34) + 22b = 8400
# 14.929,411 - 185,23b + 22b = 8400
# -163,23b = -6.529,411
# b = 40
def solve(machine: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    button_a: Tuple[int, int] = machine[0]
    button_b: Tuple[int, int] = machine[1]
    prize: Tuple[int, int] = machine[2]
    one_b: float = button_a[0] * (- button_b[1] / button_a[1]) + button_b[0]
    numbers: float = prize[0] - button_a[0] * (prize[1] / button_a[1])
    b = round(numbers / one_b)

    a = round((prize[0] - b * button_b[0]) / button_a[0])

    if a * button_a[0] + b * button_b[0] == prize[0] and a * button_a[1] + b * button_b[1] == prize[1]:
        return a, b
    return None


def determinant(matrix: List[List[int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def cramer(machine: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    button_a: Tuple[int, int] = machine[0]
    button_b: Tuple[int, int] = machine[1]
    prize: Tuple[int, int] = machine[2]

    numerator_one: List[List[int]] = [
        [prize[0], button_b[0]],
        [prize[1], button_b[1]],
    ]
    numerator_two: List[List[int]] = [
        [button_a[0], prize[0]],
        [button_a[1], prize[1]],
    ]
    denominator: List[List[int]] = [
        [button_a[0], button_b[0]],
        [button_a[1], button_b[1]],
    ]
    a: int = round(determinant(numerator_one) / determinant(denominator))
    b: int = round(determinant(numerator_two) / determinant(denominator))
    if a and b:
        if a * button_a[0] + b * button_b[0] == prize[0] and a * button_a[1] + b * button_b[1] == prize[1]:
            return a, b
    return None


def first_part():
    machines: List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]] = get_machines()
    tokens: int = 0
    for machine in machines:
        solution: Optional[Tuple[int, int]] = cramer(machine=machine)
        if solution:
            press_a, press_b = solution
            tokens += 3 * press_a + press_b
    print("tokens", tokens)


def second_part():
    machines: List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]] = get_machines()
    tokens: int = 0
    for machine in machines:
        prize: Tuple[int, int] = machine[2]
        prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        solution: Optional[Tuple[int, int]] = solve(machine=(machine[0], machine[1], prize))
        if solution:
            press_a, press_b = solution
            tokens += 3 * press_a + press_b
    print("tokens", tokens)
    pass


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
