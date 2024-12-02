from typing import List, Optional


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def first_part():
    lines = lines_of_file("first.txt")
    safe_lines: int = 0
    unsafe_lines: List[List[int]] = []
    for line in lines:
        numbers: List[int] = [int(i) for i in line.split(" ")]
        if is_safe(numbers=numbers):
            safe_lines += 1
        else:
            unsafe_lines.append(numbers)
    print("safe:", safe_lines)


def is_safe(numbers: List[int]) -> bool:
    safe: bool = True
    difference: Optional[int] = None
    last_number: Optional[int] = None
    for number in numbers:
        if last_number:
            tmp: int = number - last_number
            if not difference:
                difference = tmp
            else:
                if difference < 0 < tmp or difference > 0 > tmp:
                    safe = False
                    # unsafe
                    break
            if abs(tmp) in [1, 2, 3]:
                difference = tmp
            else:
                safe = False
        last_number = number
        if not safe:
            break
    return safe

def compare_to_previous(number: int, last: int, ascending: List[int], descending: List[int]) -> (List[int], List[int]):
    tmp: int = number - last
    if tmp > 0 and abs(tmp) in [1, 2, 3]:
        if len(ascending) == 0:
            ascending.append(last)
        if abs(number - ascending[-1]) not in [1, 2, 3]:
            pass
        elif ascending[-1] > number:
            ascending[-1] = number
        else:
            ascending.append(number)
    if tmp < 0 and abs(tmp) in [1, 2, 3]:
        if len(descending) == 0:
            descending.append(last)
        if abs(number - descending[-1]) not in [1, 2, 3]:
            pass
        elif descending[-1] < number:
            descending[-1] = number
        else:
            descending.append(number)
    return ascending, descending

def second_part():
    lines = lines_of_file("first.txt")
    safe_lines: List[List[int]] = []
    unsafe_lines: List[List[int]] = []
    for line in lines:
        numbers: List[int] = [int(i) for i in line.split(" ")]
        one_before: Optional[int] = None
        last_number: Optional[int] = numbers.pop(0)
        tmp_numbers: List[int] = [int(i) for i in line.split(" ")]
        descending: List[int] = []
        ascending: List[int] = []
        for number in numbers:
            (ascending, descending) = compare_to_previous(number, last_number, ascending, descending)
            if one_before:
                (ascending, descending) = compare_to_previous(number, one_before, ascending, descending)
            one_before = last_number
            last_number = number

        safe = len(numbers) == len(ascending) or len(numbers) == len(descending) or len(tmp_numbers) == len(
            ascending
            ) or len(tmp_numbers) == len(descending)
        if safe:
            safe_lines.append(tmp_numbers)
        else:
            unsafe_lines.append(tmp_numbers)

    print("safe:", len(safe_lines))


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
