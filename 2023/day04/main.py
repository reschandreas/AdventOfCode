"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
from typing import Tuple

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.
import utils
import re


def get_card_id_remove_prefix(line: str) -> Tuple[int, str]:
    print(line)
    id: int = int(re.findall(r"Card\ *(\d+):", line)[0])
    postfix: str = line.split(":")[1]
    return id, postfix

def first():
    value: str = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    overall: int = 0
    for line in utils.lines_of_file('first.txt'):
    # for line in utils.get_lines(value):
        id, card = get_card_id_remove_prefix(line)

        candidates, winners = card.split('|')
        candidates = [int(c) for c in re.findall(f"(\d+)", candidates)]
        winners = [int(w) for w in re.findall(f"(\d+)", winners)]
        matches: [int] = [c for c in candidates if c in winners]
        print(matches)
        linewin: int = pow(2, max(len(matches) - 1, 0)) if matches else 0
        print(linewin)
        overall += linewin
    print(f"Overall: {overall}")


def second():
    value: str = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    cards = []
    for line in utils.lines_of_file('second.txt'):
    # for line in utils.get_lines(value):
        id, card = get_card_id_remove_prefix(line)

        candidates, winners = card.split('|')
        candidates = [int(c) for c in re.findall(f"(\d+)", candidates)]
        winners = [int(w) for w in re.findall(f"(\d+)", winners)]
        matches: [int] = [c for c in candidates if c in winners]
        cards.append((id, candidates, winners, matches))
        print(matches)
        linewin: int = len(matches) if matches else 0
        print(linewin)

    og_length: int = len(cards)
    og_cards = cards.copy()
    i: int = 0
    while i < len(cards):
        id, candidates, winners, matches = cards[i]
        won: int = len(matches)
        if won == 0:
            i += 1
            continue
        og_length += won
        elements = og_cards[id:id+won]
        cards[(i+1):(i+1)] = elements
        i += 1


    print(f"Overall {len(cards)}")


if __name__ == '__main__':
    first()
    second()
