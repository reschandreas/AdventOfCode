from typing import List, Dict, Tuple


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_input() -> List[int]:
    return [int(stone) for stone in lines_of_file("first.txt")[0].split(" ")]


def apply_rule_to_number(number: int) -> List[int]:
    if number == 0:
        return [1]
    if number >= 10:
        string: str = str(number)
        length: int = len(string)
        if length % 2 == 0:
            tmp: List[str] = [c for c in string]
            middle: int = int(length / 2)
            first: str = "".join(tmp[:middle])
            second: str = "".join(tmp[middle:])
            return [int(first), int(second)]
    return [number * 2024]


def blink(stones: List[int]) -> List[int]:
    after_blinking: List[int] = []
    for stone in stones:
        tmp: List[int] = apply_rule_to_number(number=stone)
        for s in tmp:
            after_blinking.append(s)
    return after_blinking


def blink182(stone: int, times: int, cache: Dict[Tuple[int, int], int]) -> int:
    if times == 1:
        return len(apply_rule_to_number(number=stone))
    results: List[int] = apply_rule_to_number(number=stone)
    if len(results) == 2:
        left_stone: int = results[0]
        right_stone: int = results[1]
        if (left_stone, times) not in cache:
            left = blink182(stone=left_stone, times=times - 1, cache=cache)
            cache[(left_stone, times)] = left
        else:
            left = cache[(left_stone, times)]
        if (right_stone, times) not in cache:
            right = blink182(stone=right_stone, times=times - 1, cache=cache)
            cache[(right_stone, times)] = right
        else:
            right = cache[(right_stone, times)]
        return left + right
    if (results[0], times) not in cache:
        tmp = blink182(stone=results[0], times=times - 1, cache=cache)
        cache[(results[0], times)] = tmp
        return tmp
    else:
        return cache[(results[0], times)]


def first_part():
    stones: List[int] = get_input()
    times: int = 25
    for blinking in range(times):
        stones = blink(stones=stones)
    print("stones", len(stones))


def second_part():
    stones: List[int] = get_input()
    cache: Dict[Tuple[int, int], int] = {}
    times: int = 75

    counter: int = 0
    for stone in stones:
        counter += blink182(stone=stone, times=times, cache=cache)
    print("stones", counter)


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
