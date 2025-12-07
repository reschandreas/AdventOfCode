from typing import List, Tuple, Dict, Set


class Recipe:
    ranges: List[Tuple[int, int]] = []
    ingredients: List[int] = []

    def __init__(self, lines: List[str]):
        self.ranges = []
        self.ingredients = []
        for line in lines:
            line = line.removesuffix("\n")
            if not line:
                continue
            if "-" in line:
                tmp: List[int] = [int(t) for t in line.split("-")]
                self.ranges.append((tmp[0], tmp[1]))
            else:
                self.ingredients.append(int(line))

    def get_fresh_ingredients(self) -> List[int]:
        fresh_ones: List[int] = []
        for ingredient in self.ingredients:
            if ingredient in fresh_ones:
                continue
            for r in self.ranges:
                if r[0] <= ingredient <= r[1]:
                    fresh_ones.append(ingredient)
                    break
        return fresh_ones

    def count_up_ranges(self):
        tmp = self.ranges.copy()
        tmp = sorted(tmp, key=lambda tup: tup[0])
        # first only merge adjacent ranges
        current_index: int = 0
        while current_index < len(tmp):
            new_range = tmp[current_index]
            a_start, a_end = tmp[current_index]
            for j, other_one in enumerate(tmp[current_index:]):
                if new_range == other_one:
                    continue
                (b_start, b_end) = other_one
                if a_start <= b_start:
                    if a_end >= b_end:
                        # a consumes b, remove b
                        del tmp[current_index + j]
                        current_index -= 1
                        break
                    if a_end >= b_start or a_end + 1 == b_end:
                        tmp[current_index] = (a_start, max(a_end, b_end))
                        a_start, a_end = tmp[current_index]
                        del tmp[current_index + j]
                        current_index -= 1
                        break

            current_index += 1
        return list(set(tmp))


    def reduce_ranges(self, original: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        combined_ranges: List[Tuple[int, int]] = original.copy()
        current_index: int = 0
        while current_index < len(combined_ranges):
            current_range: Tuple[int, int] = combined_ranges[current_index]
            a_start, a_end = current_range
            for index, compare in enumerate(combined_ranges):
                b_start, b_end = compare
                if a_start == b_start and a_end == b_end:
                    continue
                if a_start <= b_start and a_end >= b_end:
                    # b is included in a
                    del combined_ranges[index]
                    current_index -= 1
                    break
                if a_start <= b_start <= a_end:
                    # they overlap
                    combined_ranges[current_index] = (a_start, b_end)
                    current_index -= 1
                    del combined_ranges[index]
                elif a_start <= b_start and a_end == b_end - 1:
                    combined_ranges[current_index] = (a_start, b_end)
                    current_index -= 1
                    del combined_ranges[index]
            current_index += 1
        return combined_ranges


    def get_all_fresh_IDs(self) -> int:
        combined_ranges = self.count_up_ranges()
        fresh_ids: List[int] = []
        for r in combined_ranges:
            fresh_ids.append(r[1] + 1 - r[0])
        return sum(fresh_ids)


def part_one():
    recipe: Recipe = Recipe(open("first.txt").readlines())
    print("result is", len(recipe.get_fresh_ingredients()))

def part_two():
    recipe: Recipe = Recipe(open("first.txt").readlines())
    print("result is", recipe.get_all_fresh_IDs())


if __name__ == '__main__':
    part_one()
    print("========")
    part_two()
