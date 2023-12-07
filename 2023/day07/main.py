"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
from functools import cmp_to_key

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.

FIVE_OF_A_KIND: int = 7
FOUR_OF_A_KIND: int = 6
FULL_HOUSE: int = 5
THREE_OF_A_KIND: int = 4
TWO_PAIR: int = 3
ONE_PAIR: int = 2
HIGH_CARD: int = 1


def get_type_of_card(deck: str) -> tuple[int, str]:
    unique: str = "".join(set(deck))
    if len(unique) == 5:
        return HIGH_CARD, 'high card'
    if len(unique) == 4:
        return ONE_PAIR, 'one pair'
    if len(unique) == 1:
        return FIVE_OF_A_KIND, 'five of a kind'
    if len(unique) == 2:
        first = deck.count(unique[0])
        second = deck.count(unique[1])
        if first == 4 or second == 4:
            return FOUR_OF_A_KIND, 'four of a kind'
        if first == 2 and second == 3 or first == 3 and second == 2:
            return FULL_HOUSE, 'full house'
    if len(unique) == 3:
        first = deck.count(unique[0])
        second = deck.count(unique[1])
        third = deck.count(unique[2])
        if first == 2:
            if second == 2 or third == 2:
                return TWO_PAIR, 'two pair'
        if second == 2:
            if first == 2 or third == 2:
                return TWO_PAIR, 'two pair'
        if third == 2:
            if first == 2 or second == 2:
                return TWO_PAIR, 'two pair'
        return THREE_OF_A_KIND, 'three of a kind'


def get_possible_value_of_card(deck: str) -> tuple[int, str]:
    if 'J' not in deck:
        v, t = get_type_of_card(deck)
        return deck, v, t
    best_value = None
    index = deck.index('J')
    values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    for value in values:
        tmp = deck[:index] + value + deck[index + 1:]
        new_value = get_possible_value_of_card(tmp)
        if best_value is None or new_value[1] >= best_value[1]:
            best_value = new_value
    return best_value



def replace_card_deck_with_numerical_values(deck: str, second: bool = False):
    return deck.replace('T', 'a').replace('J', 'b' if not second else '1').replace('Q', 'c').replace('K', 'd').replace('A', 'e')


def compare(a, b):
    for i in range(5):
        ta = a[1][i]
        tb = b[1][i]
        if ta < tb:
            return -1
        elif ta > tb:
            return 1

    if a[0] is None:
        return 0
    new_a, _, _, _ = a
    new_b, _, _, _ = b
    return compare((None, new_a.replace('b', '1'), None), (None, new_b.replace('b', '1'), None))


def first():
    value: str = open("first.txt", "r").read()
    cards: list = [(*get_type_of_card(line.split(' ')[0]), line.split(' ')[0],
                    replace_card_deck_with_numerical_values(line.split(' ')[0]), int(line.split(' ')[1])) for line in
                   value.splitlines()]
    buckets: dict = {}
    for i in range(1, 8):
        buckets[i] = [(deck, numdeck, bid) for order, string, deck, numdeck, bid in cards if order == i]

    overall = 0
    rank = 0
    for b in range(1, 8):
        bucket = sorted(buckets[b], key=cmp_to_key(compare))
        buckets[b] = bucket
        for deck, n, bid in bucket:
            rank += 1
            overall += bid * rank
    print(f"overall value: {overall}")


def second():
    value: str = open("first.txt", "r").read()
    cards: list = [(*get_possible_value_of_card(line.split(' ')[0]), line.split(' ')[0], int(line.split(' ')[1])) for line in
                   value.splitlines()]
    buckets: dict = {}
    for i in range(1, 8):
        buckets[i] = [(deck, replace_card_deck_with_numerical_values(deck, True), bid) for newdeck, order, string, deck, bid in cards if order == i]

    overall = 0
    rank = 0
    for b in range(1, 8):
        bucket = sorted(buckets[b], key=cmp_to_key(compare))
        buckets[b] = bucket
        for old, n, bid in bucket:
            rank += 1
            overall += bid * rank
    print(f"overall value: {overall}")


if __name__ == '__main__':
    # first()
    second()
