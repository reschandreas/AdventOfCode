import itertools
from typing import List


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())

def is_correct_order(result: int, parts: List[int], operators: List[str], acc: int) -> bool:
    if len(parts) == 0:
        return result == acc
    operator: str = operators.pop(0)
    tmp: int = parts.pop(0)
    if operator == '*':
        tmp *= acc
    if operator == '+':
        tmp += acc
    if tmp > result:
        return False
    return is_correct_order(result, parts, operators, tmp)

def is_second_correct_order(result: int, parts: List[int], operators: List[str], acc: int) -> bool:
    if len(parts) == 0:
        return result == acc
    operator: str = operators.pop(0)
    right: int = parts.pop(0)
    if operator == '*':
        acc *= right
    elif operator == '+':
        acc += right
    elif operator == '||':
        acc = int(str(int(acc)) + str(right))
    if acc > result:
        return False
    if len(operators) == 0:
        return acc == result
    return is_second_correct_order(result, parts, operators, acc)


def possible_makeups(length: int) -> List[List[str]]:
    tmp: List[List[str]] = []
    for value in list(itertools.product('+*', repeat=length)):
        t: List[str] = []
        for i in value:
            t.append(i)
        tmp.append(t)
    return tmp

def possible_second_makeups(length: int):
    tmp: List[List[str]] = []
    for value in list(itertools.product('+*o', repeat=length)):
        t: List[str] = []
        for i in value:
            t.append(i.replace('o', '||'))
        tmp.append(t)
    return tmp

def first_part():
    lines: List[(int, List[int])] = [(int(line.split(':')[0]), [int(c) for c in line.split(':')[1].strip().split(' ')])for line in lines_of_file("first.txt")]
    product: int = 0
    permutations: dict[int, List[List[str]]] = {}
    invalid: List[(int, List[int])] = []
    for result, parts in lines:
        if len(parts) - 1 not in permutations:
            permutations[len(parts) - 1] = possible_makeups(len(parts) - 1)
        possible_operators: List[List[str]] = permutations[len(parts) - 1]
        tmp = parts.copy()
        first = tmp.pop(0)
        already_counted: bool = False
        for p in possible_operators:
            if is_correct_order(result, tmp.copy(), p.copy(), first):
                if not already_counted:
                    already_counted = True
                    product += result
                    break
        if not already_counted:
            invalid.append((result, parts))
        # print(f"{result} -> {parts}: {possible_operators}")
    return product, invalid

def second_part():
    (product, lines) = first_part()
    # lines: List[(int, List[int])] = [(int(line.split(':')[0]), [int(c) for c in line.split(':')[1].strip().split(' ')])
    #                                  for line in lines_of_file("first.txt")]
    permutations: dict[int, List[List[str]]] = {}
    for result, parts in lines:
        if len(parts) - 1 not in permutations:
            permutations[len(parts) - 1] = possible_second_makeups(len(parts) - 1)
        possible_operators: List[List[str]] = permutations[len(parts) - 1]
        tmp = parts.copy()
        already_counted: bool = False
        first: int = tmp.pop(0)
        for p in possible_operators:
            if '||' not in p:
                # we already had those
                continue
            if is_second_correct_order(result, tmp.copy(), p.copy(), first):
                if not already_counted:
                    already_counted = True
                    product += result
                    break
    print(product)


def main():
    (product, _) = first_part()
    print(product)
    second_part()


if __name__ == "__main__":
    main()
