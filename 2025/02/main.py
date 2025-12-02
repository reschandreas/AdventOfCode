from typing import List
import itertools

class Range:
    start: int
    end: int

    def __init__(self, input: str):
        array: List[str] = input.split("-")
        self.start = int(array[0])
        self.end = int(array[1])


def get_ranges(file: str) -> List[Range]:
    tmp = open(f"{file}.txt", "r").read().split(",")
    ranges: List[Range] = []
    for line in tmp:
        ranges.append(Range(line))
    return ranges

def get_invalid_in_range(input: Range) -> int:
    result: int = 0
    for num in range(input.start, input.end + 1):
        tmp: str = str(num)
        half: int = len(tmp) // 2
        first: str = tmp[:half]
        second: str = tmp[half:]
        if first == second and len(first) == len(second):
            result += num
    return result

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_invalid_in_range_two(input: Range) -> int:
    result: int = 0
    for num in range(input.start, input.end + 1):
        tmp: str = str(num)
        chunk_size: int = len(tmp) // 2
        was_invalid: bool = False
        while chunk_size > 0:
            c = chunks(tmp, chunk_size)
            array: List[str] = list(c)
            was_invalid = all([array[0] == c for c in array])
            if was_invalid:
                break
            chunk_size -= 1
        if was_invalid:
            result += num
    return result


def part_one():
    ranges: List[Range] = get_ranges("first")
    result: int = 0
    for r in ranges:
        result += get_invalid_in_range(r)
    print("result is", result)

def part_two():
    ranges: List[Range] = get_ranges("first")
    result: int = 0
    for r in ranges:
        result += get_invalid_in_range_two(r)
    print("result is", result)


# too low 5352
if __name__ == '__main__':
    part_one()
    print("========")
    part_two()