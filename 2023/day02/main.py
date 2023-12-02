"""
https://stackoverflow.com/a/56185125
"""
import sys
import os
from typing import Tuple

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.
import utils
import re


def get_game_id_remove_prefix(line: str) -> Tuple[int, str]:
    id: int = int(re.findall(r"Game (\d+):", line)[0])
    postfix: str = line.removeprefix(f"Game {id}: ")
    return id, postfix


def get_sets(line: str) -> list[list[str]]:
    items: list[list[str]] = []
    for set in line.split(";"):
        items.append(re.findall(r"(\d+ \w+)", set.strip()))
    return items


def get_max_number_per_color(sets: list[list[str]]) -> dict[str, int]:
    result: dict[str, int] = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for set in sets:
        for entries in set:
            amount, color = re.findall(r"(\d+) (\w+)", entries)[0]
            result[color] = max(result[color], int(amount))
    return result


def was_possible(color_amounts: dict[str, int]) -> bool:
    return color_amounts['red'] <= 12 and color_amounts['green'] <= 13 and color_amounts['blue'] <= 14


def first():
    first: str = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    sum: int = 0
    for line in utils.get_lines(first):
        id, line = get_game_id_remove_prefix(line)
        sets: list[list[str]] = get_sets(line)
        color_amounts: dict[str, int] = get_max_number_per_color(sets)
        if was_possible(color_amounts=color_amounts):
            sum += id
    print(f"Overall: {sum}")

def second():
    second: str = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    sum: int = 0
    for line in utils.lines_of_file('second.txt'):
        id, line = get_game_id_remove_prefix(line)
        sets: list[list[str]] = get_sets(line)
        color_amounts: dict[str, int] = get_max_number_per_color(sets)
        sum += color_amounts['red'] * color_amounts['blue'] * color_amounts['green']
    print(f"Overall: {sum}")

if __name__ == '__main__':
    # first()
    second()
