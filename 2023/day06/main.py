"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
from typing import Tuple

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.
import re

def first():
    value: str = """Time:      7  15   30
Distance:  9  40  200"""

    input_value: str = """Time:        50     74     86     85
Distance:   242   1017   1691   1252"""
    overall: int = 0
    value = input_value.split("\n")
    times = [int(v) for v in re.findall("(\d+)", value[0].replace("Time:", "").strip())]
    distances = [int(v) for v in re.findall("(\d+)", value[1].replace("Distance:", "").strip())]

    print(times)
    print(distances)

    beat = []
    for index in range(len(times)):
        if index == 1:
            index = index
        distance: int = distances[index]
        time: int = times[index]
        print(f"{time}ms for {distance}mm")
        possibility_counter = 0
        found_window = False
        for pushed in range(1, int(distance / 2)):
            speed = pushed
            remaining = time - pushed
            if speed * remaining < distance or remaining <= 0 or pushed > time:
                print("skipped")
                if found_window:
                    break
                continue
            travelled = remaining * speed

            if travelled >= distance:
                possibility_counter += 1
                found_window = True
                print(f"pushed: {pushed}, with remaining time {remaining}, beat record by: {travelled - distance}")
        beat.append(possibility_counter)

    product: int = 1
    print(beat)
    for p in beat:
        product *= p
    print(f"overall {product}")


def second():
    value: str = """Time:      7  15   30
    Distance:  9  40  200"""

    input_value: str = """Time:        50     74     86     85
    Distance:   242   1017   1691   1252"""
    overall: int = 0
    value = input_value.replace(" ", "").split("\n")
    times = [int(v) for v in re.findall("(\d+)", value[0].replace("Time:", "").strip())]
    distances = [int(v) for v in re.findall("(\d+)", value[1].replace("Distance:", "").strip())]

    print(times)
    print(distances)

    beat = []
    for index in range(len(times)):
        if index == 1:
            index = index
        distance: int = distances[index]
        time: int = times[index]
        print(f"{time}ms for {distance}mm")
        possibility_counter = 0
        found_window = False
        for pushed in range(1, int(distance / 2)):
            speed = pushed
            remaining = time - pushed
            if speed * remaining < distance or remaining <= 0 or pushed > time:
                if found_window:
                    break
                continue
            travelled = remaining * speed

            if travelled >= distance:
                possibility_counter += 1
                found_window = True
        beat.append(possibility_counter)

    product: int = 1
    print(beat)
    for p in beat:
        product *= p
    print(f"overall {product}")


if __name__ == '__main__':
    #first()
    second()
