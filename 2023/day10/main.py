"""
https://stackoverflow.com/a/56185125
"""
import os
import sys
from typing import Optional

sys.path.append(os.path.join(os.path.pardir, "utils"))  # Adds higher directory to python modules path.

WEST_INDEX = 1
NORTH_INDEX = 2
EAST_INDEX = 3
SOUTH_INDEX = 4


def get_connecting_neighbors(
    node: ((str, Optional[int], Optional[int], Optional[int], Optional[int]), int, int),
    map: [[(str, Optional[int], Optional[int], Optional[int], Optional[int])]]
    ) -> []:
    neighbors = []
    node, x, y, steps = node
    # look left
    if node[WEST_INDEX] is not None and x > 0:
        if map[y][x - 1][0][EAST_INDEX] is not None:
            neighbor, nx, ny, nsteps = map[y][x - 1]
            neighbors.append((neighbor, nx, ny, max(steps + 1, nsteps)))
    # look up
    if node[NORTH_INDEX] is not None and y > 0:
        if map[y - 1][x][0][SOUTH_INDEX] is not None:
            neighbor, nx, ny, nsteps = map[y - 1][x]
            neighbors.append((neighbor, nx, ny, max(steps + 1, nsteps)))
    # look right
    if node[EAST_INDEX] is not None and x < len(map[y]) - 1:
        if map[y][x + 1][0][WEST_INDEX] is not None:
            neighbor, nx, ny, nsteps = map[y][x + 1]
            neighbors.append((neighbor, nx, ny, max(steps + 1, nsteps)))
    # look down
    if node[SOUTH_INDEX] is not None and y < len(map) - 1:
        if map[y + 1][x][0][NORTH_INDEX] is not None:
            neighbor, nx, ny, nsteps = map[y + 1][x]
            neighbors.append((neighbor, nx, ny, max(steps + 1, nsteps)))
    neighbors.sort(key=lambda n: n[3])
    return neighbors


def a_star(start, map) -> (int, list):
    open_nodes = [start]
    longest_paths = {0: [start]}
    traversed = []
    steps = 0

    while len(open_nodes) > 0:
        current = open_nodes[0]
        if current == start and steps > 0:
            return current[3]
        open_nodes.remove(current)
        for neighbor in get_connecting_neighbors(current, map):
            node, nx, ny, nsteps = neighbor
            if nsteps >= steps and (node, nx, ny) not in traversed:
                if neighbor[0] != START:
                    open_nodes.append(neighbor)
                steps = nsteps
                if steps not in longest_paths:
                    longest_paths[steps] = longest_paths[steps - 1]
                    del longest_paths[steps - 1]

                longest_paths[steps].append(neighbor)
            traversed.append((node, nx, ny))
    return steps, longest_paths[steps]


VERTICAL = ('|', None, -1, None, 1)
HORIZONTAL = ('─', -1, None, 1, None)
L_SHAPED = ('└', None, -1, 1, None)
SEVEN_SHAPED = ('┐', -1, None, None, 1)
F_SHAPED = ('┌', None, None, 1, 1)
J_SHAPED = ('┘', -1, 1, None, None)
GROUND = ('.', None, None, None, None)
START = ('S', -1, -1, 1, 1)


def get_type_of_pipe(char: str):
    if char == START[0]:
        return START
    if char == '.':
        return GROUND
    if char == '|':
        return VERTICAL
    if char == '-':
        return HORIZONTAL
    if char == 'L':
        return L_SHAPED
    if char == 'J':
        return J_SHAPED
    if char == '7':
        return SEVEN_SHAPED
    if char == 'F':
        return F_SHAPED
    raise Exception(f"the hell {char}?!")


def parse_map(lines: str) -> ([[(str, Optional[int], Optional[int], Optional[int], Optional[int])]],
                              (str, Optional[int], Optional[int], Optional[int], Optional[int])):
    map: [[((str, Optional[int], Optional[int], Optional[int], Optional[int]), int, int)]] = []
    start = None
    x: int = 0
    y: int = 0
    for line in lines.splitlines():
        new_line = []
        x = 0
        for char in line:
            pipetype = get_type_of_pipe(char)
            if pipetype == START:
                start = (pipetype, x, y, 0)
            new_line.append((pipetype, x, y, 0))
            x += 1
        map.append(new_line)
        y += 1
    return map, start


def first():
    value: str = """.....
.S-7.
.|.|.
.L-J.
....."""
    value = open("first.txt").read()
    map, start = parse_map(lines=value)
    steps, _ = a_star(start, map)
    print(steps)


def second():
    value: str = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    value: str = """...........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""
    value: str = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    value: str = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    value = open("first.txt").read()
    map, start = parse_map(lines=value)
    steps, path = a_star(start, map)
    enclosed = replace_ins_and_outs(path, map)
    print(enclosed)


def replace_ins_and_outs(path, map):
    new_map = []
    enclosed = 0
    y: int = 0
    path_nodes = [(node, nx, ny) for node, nx, ny, _ in path]
    last_line = []
    for line in map:
        x: int = 0
        new_line = []
        im_in = False
        inbetween = 0
        for node in line:
            node, origx, origy, _ = node
            if (node, origx, origy) not in path_nodes:
                if y > 0:
                    if last_line[x][0] == 'O' or last_line[x][0] == 'I':
                        im_in = last_line[x][0] == 'I'
                        inbetween = 0
                if inbetween % 2 == 1 and inbetween > 0:
                    im_in = not im_in
                    inbetween = 0
                new_line.append(('I' if im_in else 'O', x, y))
                if im_in:
                    enclosed += 1
                    inbetween = 0
            else:
                new_line.append((node[0][0], origx, origy))
                if node not in [HORIZONTAL, L_SHAPED, J_SHAPED]:
                    inbetween += 1
            x += 1
        new_map.append(new_line)
        last_line = new_line
        y += 1
    for line in new_map:
        for (n, x, y) in line:
            print(n, end='')
        print('')
    return enclosed


if __name__ == '__main__':
    # first()
    second()
