from typing import List, Tuple

class Battery:
    values: List[int] = []

    def __init__(self, array: str):
        self.values = []
        for i in array:
            self.values.append(int(i))

    def find_highest(self, haystack: List[int]) -> Tuple[int, int]:
        if len(haystack) == 0:
            raise
        max: int = haystack[0]
        max_index = 0
        if max == 9:
            return max, max_index
        for index, i in enumerate(haystack):
            if i > max:
                max = i
                max_index = index
                if max == 9:
                    return max, max_index
        return max, max_index


    def joltage(self) -> int:
        haystack: List[int] = self.values[:-1]
        (ten, ten_index) = self.find_highest(haystack)
        haystack: List[int] = self.values[ten_index + 1:]
        (digit, digit_index) = self.find_highest(haystack)
        return ten * 10 + digit

    def max_joltage(self) -> int:
        result: str = ""
        real_index = 0
        for i in range(12):
            if len(result) == 12:
                break
            skip_last: int = 12 - len(result) - 1
            tmp: List[int] = self.values[real_index:-skip_last]
            if skip_last == 0:
                tmp = self.values[real_index:]
            (_next, next_index) = self.find_highest(tmp)
            result += str(_next)
            real_index += next_index + 1
        return int(result)


def get_batteries(file: str) -> List[Battery]:
    tmp = open(f"{file}.txt", "r").readlines()
    batteries: List[Battery] = []
    for line in tmp:
        batteries.append(Battery(line.removesuffix("\n")))
    return batteries


def part_one():
    batteries: List[Battery] = get_batteries("first")
    result: int = 0
    for battery in batteries:
        result += battery.joltage()
    print("result is", result)

def part_two():
    batteries: List[Battery] = get_batteries("first")
    result: int = 0
    for battery in batteries:
        result += battery.max_joltage()
    print("result is", result)


if __name__ == '__main__':
    part_one()
    print("========")
    part_two()