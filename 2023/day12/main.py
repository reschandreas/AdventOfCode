"""
https://stackoverflow.com/a/56185125
"""
import os
import sys

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.


def get_lines(string: str) -> [([str], [int])]:
    lines = []
    for line in string.splitlines():
        array = line.split(" ")
        puzzle: [str] = [c for c in array[0]]
        numbers: [int] = [int(n) for n in array[1].split(",")]
        lines.append((puzzle, numbers))
    return lines

def check_line(line: [str], groups: [int]) -> bool:
    group = 0
    for i in range(len(line)):
        if line[i] == '.':
            group = groups.pop(0)
        if group > 0 and line[i] != '.':
            return False
        else:
            group -= 1
    return True

def get_permutations(array: [str], must_fit: [int]) -> [str]:
    possibility = []
    return possibility


def first():
    value: str = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    lines = get_lines(value)
    for (puzzle, numbers) in lines:
        print(check_line(['#','.','#','.','#','#''#'], numbers))
        print(check_line(['.','#','#','.','#','#''#'], numbers))
        # (12 - 3 - (1 + 2 + 3)) * 3
        # 14-5*1-2-3 maybe? 2 line
        # (|? in einer reihe| - |je gruppe die möglich|)*|gruppen die möglich|
        string = "".join(puzzle)
        groups = get_groups_of_question(string)
        for group in groups:
            sum = 0
            amount = 0
            for s in numbers:
                if s == len(group):
                    sum += s
                    amount += 1
                    break
                if sum + s < len(group):
                    sum += s
                    amount += 1
                else:
                    break
            idea = (len(group) - sum) * amount
        number_of_questions = "".join(puzzle).count("?")
        total = len(puzzle)
        groups = len(numbers)
        print(numbers, puzzle)


def get_groups_of_question(string: str) -> [str]:
    array: [str] = []
    new_group: [str] = []
    for c in string:
        if not new_group and c == '?':
            new_group = [c]
        elif new_group and c == '?':
            new_group.append(c)
        if c != '?':
            if new_group:
                array.append(new_group)
                new_group = []
    if new_group:
        array.append(new_group)
    return array


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
    # value = open("first.txt").read()


if __name__ == '__main__':
    first()
    # second()
