from enum import Enum
from typing import List


class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class Rotation:
    direction: Direction
    amount: int

    def __init__(self, input: str):
        direction: str = input[0]
        self.direction = Direction.LEFT if direction == 'L' else Direction.RIGHT
        self.amount = int(input[1:])


def get_rotations(file: str) -> List[Rotation]:
    lines = open(f"{file}.txt", "r").readlines()
    rotations: List[Rotation] = []
    for line in lines:
        rotations.append(Rotation(line))
    return rotations


def rotate(position: int, direction: Direction, amount: int) -> int:
    position += direction.value * amount
    return position % 100

def part_one():
    instructions: List[Rotation] = get_rotations("first")
    position: int = 50
    result: int = 0
    for instruction in instructions:
        value = rotate(position, instruction.direction, instruction.amount)
        if value == 0:
            result += 1
        position = value
    print("result is", result)

def pointed_at_zero(position: int, rotation: Rotation) -> int:
    value = 0
    for i in range(rotation.amount):
        position += rotation.direction.value
        if position % 100 == 0:
            value += 1
    if position % 100 == 0:
        value -= 1
    return value

def part_two():
    instructions: List[Rotation] = get_rotations("first")
    position: int = 50
    result: int = 0
    for instruction in instructions:
        value = rotate(position, instruction.direction, instruction.amount)
        additional = pointed_at_zero(position, instruction)
        result += additional
        if value == 0:
            result += 1
        position = value
    print("result is", result)


# too low 5352
if __name__ == '__main__':
    part_one()
    print("========")
    part_two()