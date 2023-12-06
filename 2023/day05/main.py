"""
https://stackoverflow.com/a/56185125
"""
import json
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
        elif len(map) > 1:
            remaining_map = map[index + 1:]
            new_index = int(len(remaining_map) / 2)
            return binary_search(new_index, remaining_map, value)
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

    headers: list[str] = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                          'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']


    already_done = 1_183_200_000 #709200000 + 107200000

    if True or not os.path.exists("seeds.json"):
        # lines: list[str] = utils.get_lines(value)
        lines: list[str] = utils.lines_of_file('first.txt')
        seeds = get_seeds(lines.pop(0))
        seed_index: int = 0
        new_seeds = []

        while seed_index < len(seeds) - 1:
            seed = seeds[seed_index]
            new_one = seeds[seed_index + 1]
            for i in range(seed, seed + new_one):
                if already_done > 0:
                    already_done -= 1
                if already_done < 10:
                    if already_done == 9:
                        print("starting")
                    new_seeds.append(i)
            seed_index += 2
            print(f"did {seed_index}")
        seeds = new_seeds
        #json.dump(new_seeds, open("seeds.json", "w"))
    else:
        print("reading seeds.json")
        seeds = json.load(open("seeds.json", "r"))
        print("read seeds.json")



    sorted: dict = {}
    if True or not os.path.exists("sorted.json"):
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

        del lines

        for header in headers:
            sorted[header] = []
            sorted_mapping = sort_for_second(mapped[header])
            sorted[header] = sorted_mapping
        del mapped
        #json.dump(sorted, open("sorted.json", "w"))
    else:
        sorted = json.load(open("sorted.json", "r"))
        pass

    lowest = None #187579915 # wrong
    print("letss goooo")
    index = 1_183_200_000
    seed_to_soil_len = int(len(sorted['seed-to-soil']) / 2)
    soil_to_fertilizer_len = int(len(sorted['soil-to-fertilizer']) / 2)
    fertilizer_to_water = int(len(sorted['fertilizer-to-water']) / 2)
    water_to_light_len = int(len(sorted['water-to-light']) / 2)
    light_to_temperature_len = int(len(sorted['light-to-temperature']) / 2)
    temp_to_humidity_len = int(len(sorted['temperature-to-humidity']) / 2)
    humidity_to_location_len = int(len(sorted['humidity-to-location']) / 2)
    cache = {}
    lowest = 658168220
    if len(sorted['humidity-to-location']) != 0:
        tmp = humidity_to_location_len
        sorted['humidity-to-location'] = remove_bigger_mappings(lowest, sorted['humidity-to-location'])
        humidity_to_location_len = int(len(sorted['humidity-to-location']) / 2)
        if tmp != humidity_to_location_len:
            print(f"removed {tmp - humidity_to_location_len} values from humidity-to-location")
    if len(sorted['humidity-to-location']) == 0:
        tmp = temp_to_humidity_len
        sorted['temperature-to-humidity'] = remove_bigger_mappings(lowest, sorted['temperature-to-humidity'])
        temp_to_humidity_len = int(len(sorted['temperature-to-humidity']) / 2)
        if tmp != temp_to_humidity_len:
            print(f"removed {tmp - temp_to_humidity_len} values from temperature-to-humidity")
    if len(sorted['temperature-to-humidity']) == 0:
        tmp = light_to_temperature_len
        sorted['light-to-temperature'] = remove_bigger_mappings(lowest, sorted['light-to-temperature'])
        light_to_temperature_len = int(len(sorted['light-to-temperature']) / 2)
        if tmp != light_to_temperature_len:
            print(f"removed {tmp - light_to_temperature_len} values from light-to-temperature")
    if len(sorted['light-to-temperature']) == 0:
        tmp = water_to_light_len
        sorted['water-to-light'] = remove_bigger_mappings(lowest, sorted['water-to-light'])
        water_to_light_len = int(len(sorted['water-to-light']) / 2)
        if tmp != water_to_light_len:
            print(f"removed {tmp - water_to_light_len} values from water-to-light")
    if len(sorted['water-to-light']) == 0:
        tmp = fertilizer_to_water
        sorted['fertilizer-to-water'] = remove_bigger_mappings(lowest, sorted['fertilizer-to-water'])
        fertilizer_to_water = int(len(sorted['fertilizer-to-water']) / 2)
        if tmp != fertilizer_to_water:
            print(f"removed {tmp - fertilizer_to_water} values from fertilizer-to-water")
    if len(sorted['fertilizer-to-water']) == 0:
        tmp = soil_to_fertilizer_len
        sorted['soil-to-fertilizer'] = remove_bigger_mappings(lowest, sorted['soil-to-fertilizer'])
        soil_to_fertilizer_len = int(len(sorted['soil-to-fertilizer']) / 2)
        if tmp != soil_to_fertilizer_len:
            print(f"removed {tmp - soil_to_fertilizer_len} values from soil-to-fertilizer")
    if len(sorted['soil-to-fertilizer']) == 0:
        tmp = seed_to_soil_len
        sorted['seed-to-soil'] = remove_bigger_mappings(lowest, sorted['seed-to-soil'])
        seed_to_soil_len = int(len(sorted['seed-to-soil']) / 2)
        if tmp != seed_to_soil_len:
            print(f"removed {tmp - seed_to_soil_len} values from seed-to-soil")
    lowest = None
    for seed in seeds:
        index += 1
        location = None
        current_value = seed
        if current_value in cache:
            location = cache[current_value]
            print(f"cache hit for seed directly {seed} -> {location}")
        if len(sorted['seed-to-soil']) == 0:
            print("all mappings exhausted")
            location = current_value
        if location is None:
            current_value = binary_search(seed_to_soil_len, sorted['seed-to-soil'], current_value)
            current_value = binary_search(soil_to_fertilizer_len, sorted['soil-to-fertilizer'], current_value)

            current_value = binary_search(fertilizer_to_water, sorted['fertilizer-to-water'], current_value)
            current_value = binary_search(water_to_light_len, sorted['water-to-light'], current_value)
            current_value = binary_search(light_to_temperature_len, sorted['light-to-temperature'], current_value)

            current_value = binary_search(temp_to_humidity_len, sorted['temperature-to-humidity'], current_value)

            location = binary_search(humidity_to_location_len, sorted['humidity-to-location'], current_value)
        cache[seed] = location
        if lowest is None or location < lowest:
            lowest = location
            if len(sorted['humidity-to-location']) != 0:
                tmp = humidity_to_location_len
                sorted['humidity-to-location'] = remove_bigger_mappings(lowest, sorted['humidity-to-location'])
                humidity_to_location_len = int(len(sorted['humidity-to-location']) / 2)
                if tmp != humidity_to_location_len:
                    print(f"removed {tmp - humidity_to_location_len} values from humidity-to-location")
            if len(sorted['humidity-to-location']) == 0:
                tmp = temp_to_humidity_len
                sorted['temperature-to-humidity'] = remove_bigger_mappings(lowest, sorted['temperature-to-humidity'])
                temp_to_humidity_len = int(len(sorted['temperature-to-humidity']) / 2)
                if tmp != temp_to_humidity_len:
                    print(f"removed {tmp - temp_to_humidity_len} values from temperature-to-humidity")
            if len(sorted['temperature-to-humidity']) == 0:
                tmp = light_to_temperature_len
                sorted['light-to-temperature'] = remove_bigger_mappings(lowest, sorted['light-to-temperature'])
                light_to_temperature_len = int(len(sorted['light-to-temperature']) / 2)
                if tmp != light_to_temperature_len:
                    print(f"removed {tmp - light_to_temperature_len} values from light-to-temperature")
            if len(sorted['light-to-temperature']) == 0:
                tmp = water_to_light_len
                sorted['water-to-light'] = remove_bigger_mappings(lowest, sorted['water-to-light'])
                water_to_light_len = int(len(sorted['water-to-light']) / 2)
                if tmp != water_to_light_len:
                    print(f"removed {tmp - water_to_light_len} values from water-to-light")
            if len(sorted['water-to-light']) == 0:
                tmp = fertilizer_to_water
                sorted['fertilizer-to-water'] = remove_bigger_mappings(lowest, sorted['fertilizer-to-water'])
                fertilizer_to_water = int(len(sorted['fertilizer-to-water']) / 2)
                if tmp != fertilizer_to_water:
                    print(f"removed {tmp - fertilizer_to_water} values from fertilizer-to-water")
            if len(sorted['fertilizer-to-water']) == 0:
                tmp = soil_to_fertilizer_len
                sorted['soil-to-fertilizer'] = remove_bigger_mappings(lowest, sorted['soil-to-fertilizer'])
                soil_to_fertilizer_len = int(len(sorted['soil-to-fertilizer']) / 2)
                if tmp != soil_to_fertilizer_len:
                    print(f"removed {tmp - soil_to_fertilizer_len} values from soil-to-fertilizer")
            if len(sorted['soil-to-fertilizer']) == 0:
                tmp = seed_to_soil_len
                sorted['seed-to-soil'] = remove_bigger_mappings(lowest, sorted['seed-to-soil'])
                seed_to_soil_len = int(len(sorted['seed-to-soil']) / 2)
                if tmp != seed_to_soil_len:
                    print(f"removed {tmp - seed_to_soil_len} values from seed-to-soil")
        if index % 100000 == 0:
            # 214922730 is too high
            # 1100841983 a
            # 658168220 a
            # 616300322 incorrect
            # 187579915 incorrect
            # 49741801 incorrect
            # 628406338 incorrect
            # 838147849 incorrect
            # 472480890 incorrect
            # 148041808 correct! first guess
            print(f"{index} and lowest is {lowest}")

    print(f"lowest is {lowest}")


def remove_bigger_mappings(lowest, mapping):
    keep = []
    for a, b, m in mapping:
        if m < lowest:
            keep.append((a, b, m))
    return keep


if __name__ == '__main__':

    second()
