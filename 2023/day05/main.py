"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
from typing import Any

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.
import utils
import re


def get_seeds(line: str) -> list[int]:
    seeds: list[int] = re.findall(r"(\d+)", line)
    return [int(s) for s in seeds]


def calculate_mapping(dest_range_start: int, source_range_start: int, length: int) -> dict:
    mapping: dict = {}
    mapping[(source_range_start, length)] = dest_range_start
    return mapping


def takeFirst(elem):
    return elem[0]


def sort_for_second(mapping: dict):
    sorted_elems = []
    for elem in mapping:
        start, length = elem
        sorted_elems.append((start, length, mapping[elem]))
    sorted_elems.sort(key=takeFirst)
    return sorted_elems


def get_mapped_value(value, source_start, length, destination_start):
    if value == source_start:
        return destination_start
    if value < source_start:
        return value
    if value <= source_start + length:
        return destination_start + (value - source_start)
    return value


def first():
    value: str = """seeds: 79 14 55 13
seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    overall: int = 0
    # for line in utils.lines_of_file('first.txt'):
    lines: list[str] = utils.get_lines(value)
    # lines: list[str] = utils.lines_of_file('first.txt')
    maps: list[list[list[int]]] = []
    headers: list[str] = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                          'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    seeds = get_seeds(lines.pop(0))
    if lines[0] == '':
        lines.pop(0)
    groups: dict[str, list[Any]] = {}
    current_needs: int = 0
    current_group: str = ""
    for line in lines:
        if line == '':
            current_needs += 1
            continue
        if line.startswith(headers[current_needs]):
            groups[headers[current_needs]] = []
            current_group = headers[current_needs]
        else:
            groups[current_group].append([int(s) for s in re.findall(r"(\d+)", line)])

    mapped: dict = {}
    for header in headers:
        mapped[header] = {}
        for entry in groups[header]:
            mapping = calculate_mapping(entry[0], entry[1], entry[2])
            mapped[header].update(mapping)

    lowest = None
    for seed in seeds:
        soil = search_match(mapped['seed-to-soil'], seed)
        fertilizer = search_match(mapped['soil-to-fertilizer'], soil)
        water = search_match(mapped['fertilizer-to-water'], fertilizer)
        light = search_match(mapped['water-to-light'], water)
        temp = search_match(mapped['light-to-temperature'], light)
        humidity = search_match(mapped['temperature-to-humidity'], temp)
        location = search_match(mapped['humidity-to-location'], humidity)
        if lowest == None:
            lowest = location
        else:
            lowest = min(lowest, location)

    print(f"Overall: {lowest}")


def search_match(map: dict, value: int, upto=None):
    tmp = value
    for entry in map:
        source_range_start, length = entry
        dest_range_start = map[(source_range_start, length)]
        newvalue = get_mapped_value(value, source_range_start, length, dest_range_start)
        if upto is not None:
            uptovalue = get_mapped_value(upto, source_range_start, length, dest_range_start)
            if uptovalue < newvalue:
                return newvalue
        if newvalue != tmp:
            return newvalue

    return value


def binary_search(index: int, map: list, value: int):
    if index >= len(map):
        return value
    start, range, mapped = map[index]
    if value < start:
        return binary_search(int(index / 2), map[:index], value)
    if start == value:
        return mapped
    if start < value:
        if value < start + range:
            return mapped + (value - start)
        else:
            return binary_search(int((index / 2) + index), map[index:], value)
    return value


def second():
    value: str = """seeds: 79 14 55 13
seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    # 214922730 is too high
    overall: int = 0
    # lines: list[str] = utils.get_lines(value)
    lines: list[str] = utils.lines_of_file('first.txt')
    headers: list[str] = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                          'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    seeds = get_seeds(lines.pop(0))
    seed_index: int = 0
    seed_ranges = []
    new_seeds = []

    while seed_index < len(seeds) - 1:
        seed = seeds[seed_index]
        new_seeds.append(seed)
        new_one = seeds[seed_index + 1]
        for i in range(seed, seed + new_one - 1):
            new_seeds.append(i)
        seed_ranges.append([seed, seed + new_one - 1])
        seed_index += 2
    seeds = new_seeds

    if lines[0] == '':
        lines.pop(0)
    groups: dict[str, list[Any]] = {}
    current_needs: int = 0
    current_group: str = ""
    for line in lines:
        if line == '':
            current_needs += 1
            continue
        if line.startswith(headers[current_needs]):
            groups[headers[current_needs]] = []
            current_group = headers[current_needs]
        else:
            groups[current_group].append([int(s) for s in re.findall(r"(\d+)", line)])

    mapped: dict = {}
    for header in headers:
        mapped[header] = {}
        for entry in groups[header]:
            mapping = calculate_mapping(entry[0], entry[1], entry[2])
            mapped[header].update(mapping)

    sorted: dict = {}
    for header in headers:
        sorted[header] = []
        sorted_mapping = sort_for_second(mapped[header])
        sorted[header] = sorted_mapping
    lowest = None
    print("letss goooo")
    for seed in seeds:
        soil = binary_search(len(sorted['seed-to-soil']) - 1, sorted['seed-to-soil'], seed)
        fertilizer = binary_search(len(sorted['soil-to-fertilizer']) - 1, sorted['soil-to-fertilizer'], soil)
        water = binary_search(len(sorted['fertilizer-to-water']) - 1, sorted['fertilizer-to-water'], fertilizer)
        light = binary_search(len(sorted['water-to-light']) - 1, sorted['water-to-light'], water)
        temp = binary_search(len(sorted['light-to-temperature']) - 1, sorted['light-to-temperature'], light)
        humidity = binary_search(len(sorted['temperature-to-humidity']) - 1, sorted['temperature-to-humidity'], temp)
        location = binary_search(len(sorted['humidity-to-location']) - 1, sorted['humidity-to-location'], humidity)
        if lowest is None or location < lowest:
            lowest = location

    print(f"lowest is {lowest}")
    # cache = {}
    # if os.path.exists("cache.json"):
    #     cache = json.load(open("cache.json", "r"))
    # print(f"read {len(cache)} from cache")
    # lowest = None
    # index = 0
    # start = time.time()
    # print("lets go")
    # for seed in seeds:
    #     upto = None
    #     for s in seed_ranges:
    #         if seed == s[0]:
    #             upto = s[1]
    #             break
    #     if seed not in cache:
    #         index += 1
    #         if index % 10_000_000 == 0 and index > 10:
    #             json.dump(cache, open("cache.json", "w"))
    #             print(f"caching {len(cache)} values")
    #         soil = search_match(mapped['seed-to-soil'], seed)
    #         fertilizer = search_match(mapped['soil-to-fertilizer'], soil)
    #         water = search_match(mapped['fertilizer-to-water'], fertilizer)
    #         light = search_match(mapped['water-to-light'], water)
    #         temp = search_match(mapped['light-to-temperature'], light)
    #         humidity = search_match(mapped['temperature-to-humidity'], temp)
    #         location = search_match(mapped['humidity-to-location'], humidity)
    #         cache[seed] = location
    #     else:
    #         print(f"cache hit for {seed}")
    #         location = cache[seed]
    #     new = seed + 1
    #     if upto is not None:
    #         while new <= upto:
    #             index += 1
    #             if index % 10_000_000 == 0 and index > 10:
    #                 json.dump(cache, open("cache.json", "w"))
    #                 print(f"caching {len(cache)} values")
    #             if new not in cache:
    #                 orig_location = location
    #                 uptosoil = search_match(mapped['seed-to-soil'], new)
    #                 if soil != uptosoil:
    #                     soil = uptosoil
    #                     fertilizer = search_match(mapped['soil-to-fertilizer'], soil)
    #                     water = search_match(mapped['fertilizer-to-water'], fertilizer)
    #                     light = search_match(mapped['water-to-light'], water)
    #                     temp = search_match(mapped['light-to-temperature'], light)
    #                     humidity = search_match(mapped['temperature-to-humidity'], temp)
    #                     location = search_match(mapped['humidity-to-location'], humidity)
    #                     cache[new] = location
    #             else:
    #                 print(f"cache hit for {new}")
    #                 location = cache[new]
    #             if location > orig_location:
    #                 location = orig_location
    #             new += 1
    #     if lowest is None:
    #         lowest = location
    #     else:
    #         lowest = min(lowest, location)
    # print(f"took only {time.time() - start}s")
    # print(f"Overall: {lowest}")


if __name__ == '__main__':
    # first()
    second()
