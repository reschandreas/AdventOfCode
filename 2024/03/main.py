import re
from typing import List, Optional


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def first_part():
    lines = lines_of_file("first.txt")
    line = lines.pop(0)
    for l in lines:
        line += l
    matches: List[str] = re.findall(r"(mul\(\d+,\d+\))", line)
    result: int = 0
    for match in matches:
        numbers: List[int] = [int(i) for i in match.removeprefix("mul(").removesuffix(")").split(",")]
        print(numbers)
        result += numbers[0] * numbers[1]
    print(result)

def second_part():
    lines = lines_of_file("first.txt")
    line = lines.pop(0)
    for l in lines:
        line += l
    matches: List[str] = re.findall(r"(mul\(\d+,\d+\))|(don't\(\))|(do\(\))", line)
    result: int = 0
    enabled: bool = True
    for match in matches:
        instruction, dont, do = match
        if dont:
            enabled = False
        if do:
            enabled = True
        if instruction and enabled:
            numbers: List[int] = [int(i) for i in instruction.removeprefix("mul(").removesuffix(")").split(",")]
            print(numbers)
            result += numbers[0] * numbers[1]
    print(result)

def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
