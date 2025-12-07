from enum import Enum
from typing import List


class Operator(Enum):
    ADD = "+"
    MULTIPLY = "*"


class Problem:
    numbers: List[int] = []
    operator: Operator

    def __init__(self, input: List[str]):
        self.operator = Operator(input.pop())
        self.numbers = [int(x) for x in input]

    def solve(self) -> int:
        if self.operator.value == Operator.ADD.value:
            return sum(self.numbers)
        if self.operator == Operator.MULTIPLY:
            result: int = 1
            for n in self.numbers:
                result *= n
            return result

class SecondProblem:

    numbers: List[int] = []
    operator: Operator

    def __init__(self, input: List[List[str]]):
        self.numbers = []
        for line in input:
            n: List[str] = []
            for l in line:
                if l == Operator.ADD.value or l == Operator.MULTIPLY.value:
                    self.operator = Operator(l)
                else:
                    n.append(l)
            self.numbers.append(int("".join(n)))
        self.numbers.reverse()

    def solve(self) -> int:
        if self.operator.value == Operator.ADD.value:
            return sum(self.numbers)
        if self.operator == Operator.MULTIPLY:
            result: int = 1
            for n in self.numbers:
                result *= n
            return result


def get_problems(file: str) -> List[Problem]:
    lines: List[List[str]] = []
    columns: List[List[str]] = []
    for line in open(f"{file}.txt").readlines():
        line = line.removesuffix("\n")
        while "  " in line:
            line = line.replace("  ", " ").strip()
        lines.append(line.split(" "))
    for i in range(len(lines[0])):
        column: List[str] = []
        for line in lines:
            column.append(line[i])
        columns.append(column)
    problems: List[Problem] = [Problem(c) for c in columns]
    return problems

def get_second_problems(file: str) -> List[SecondProblem]:
    lines: List[str] = []
    columns: List[List[str]] = []
    for line in open(f"{file}.txt").readlines():
        line = line.removesuffix("\n")
        lines.append(line)
    length: int = max([len(line) for line in lines])
    amount_of_lines = len(lines)
    for col in range(length):
        column: List[str] = []
        for c in range(amount_of_lines):
            if col >= len(lines[c]):
                column.append(" ")
            else:
                column.append(lines[c][col])
        columns.append(column)
    problem_sets: List[List[List[str]]] = []
    working_set: List[List[str]] = []
    for col in columns:
        if "" == "".join(col).strip():
            problem_sets.append(working_set)
            working_set = []
        else:
            working_set.append(col)
    problem_sets.append(working_set)
    problems: List[SecondProblem] = [SecondProblem(c) for c in problem_sets]
    return problems


def part_one():
    problems: List[Problem] = get_problems("first")
    result: int = 0
    for problem in problems:
        result += problem.solve()
    print("result is", result)


def part_two():
    problems: List[SecondProblem] = get_second_problems("first")
    result: int = 0
    problems.reverse()
    for problem in problems:
        tmp = problem.solve()
        result += tmp
    print("result is", result)


if __name__ == '__main__':
    part_one()
    print("========")
    part_two()
