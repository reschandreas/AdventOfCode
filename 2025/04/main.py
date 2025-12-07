from enum import Enum
from typing import List, Tuple


class Item(Enum):

    PaperRoll = '@'
    Empty = '.'
    Marked = 'x'

class Map:

    layout: List[List[Item]]
    visualized: List[List[Item]]

    def __init__(self, lines: List[str]) -> None:
        self.layout = []
        self.visualized = []
        for line in lines:
            mapped: List[Item] = [Item(x) for x in line.removesuffix("\n")]
            self.layout.append(mapped)
            self.visualized.append([Item(x) for x in line.removesuffix("\n")])

    def can_be_accessed(self, row: int, column: int) -> bool:
        if row == 0 and column == 7:
            row = 0
        if self.layout[row][column] == Item.Empty:
            return False
        counter: int = 0

        prev_row: int = max(0, row - 1)
        prev_col: int = max(0, column - 1)

        indices_to_check: List[List[Tuple[int, int]]] = [
            [(prev_row, prev_col), (prev_row, column), (prev_row, column + 1)],
            [(row, prev_col), (row, column + 1)],
            [(row + 1, prev_col), (row + 1, column), (row + 1, column + 1)],
        ]
        # if we are in the first column, we dont need to check stuff on the left, same on the right
        if column == 0:
            for i in range(3):
                indices_to_check[i].pop(0)
        elif column == len(self.layout[0]) - 1:
            for i in range(3):
                indices_to_check[i].pop()
        # if we are on top, we can skip all the ones above
        if row == 0:
            indices_to_check[0] = []
        #if we are on the bottom, we can skip the ones below
        if row == len(self.layout) - 1:
            indices_to_check[2] = []

        for check in indices_to_check:
            for x, y in check:
                if self.layout[x][y] == Item.PaperRoll:
                    counter += 1
        return counter < 4


    def run_over_map(self) -> int:
        counter: int = 0
        for row in range(len(self.layout)):
            for column in range(len(self.layout[0])):
                if self.can_be_accessed(row, column):
                    counter += 1
                    self.visualized[row][column] = Item.Marked
        return counter

    def run_over_map_and_remove(self) -> int:
        counter: int = 0
        previous_counter: int = -1
        while counter != previous_counter:
            previous_counter = counter
            counter = 0
            for row in range(len(self.layout)):
                for column in range(len(self.layout[0])):
                    if self.can_be_accessed(row, column):
                        counter += 1
                        self.visualized[row][column] = Item.Marked
                        # removes the need to iterate over it all the time
                        self.layout[row][column] = Item.Marked
        return counter

    def visualize(self):
        for row in self.visualized:
            print("".join([x.value for x in row]))


def get_map(file: str) -> Map:
    lines: List[str] = open(f"{file}.txt").readlines()
    return Map(lines)


def part_one():
    m: Map = get_map("first")
    result: int = m.run_over_map()
    m.visualize()
    print("result is ", result)

def part_two():
    m: Map = get_map("first")
    result: int = m.run_over_map_and_remove()
    m.visualize()
    print("result is ", result)


if __name__ == '__main__':
    part_one()
    print("========")
    part_two()