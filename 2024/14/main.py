from time import sleep
from typing import List, Tuple


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_robot(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    parts: List[str] = line.split(" ")
    coordinates: List[int] = [int(p) for p in parts[0].removeprefix("p=").split(",")]
    speed: List[int] = [int(v) for v in parts[1].removeprefix("v=").split(",")]
    return (coordinates[0], coordinates[1]), (speed[0], speed[1])


def get_robots() -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    robots: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    for line in get_input():
        robots.append(get_robot(line=line))
    return robots


def location_after(robot: Tuple[Tuple[int, int], Tuple[int, int]], iterations: int, width: int, height: int) -> Tuple[
    int, int]:
    coordinates: Tuple[int, int] = robot[0]
    speed: Tuple[int, int] = robot[1]
    return (coordinates[0] + speed[0] * iterations) % width, (coordinates[1] + speed[1] * iterations) % height


def should_print_matrix(width: int, height: int, locations: List[Tuple[int, int]]):
    for i in range(height):
        line: str = ''
        for j in range(width):
            if (j, i) in locations:
                line += '1'
            else:
                line += ' '
        if "1111111111111111111111111111111" in line:
            return True
    return False

def print_matrix(width: int, height: int, locations: List[Tuple[int, int]]):
    for i in range(height):
        line: str = ''
        for j in range(width):
            if (j, i) in locations:
                line += '1'
            else:
                line += ' '
        print(line)


def get_input() -> List[str]:
    matrix: List[str] = []
    for line in lines_of_file("first.txt"):
        matrix.append(line)
    return matrix


def get_robot_locations(robots: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> List[Tuple[int, int]]:
    return [r[0] for r in robots]


def count_in_quadrant(width: int, height: int, locations: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    half_width: int =  height // 2
    half_height: int =  width // 2
    left_up: List[Tuple[int, int]] = [(x, y) for (x, y) in locations if x < half_height and y < half_width]
    left_down: List[Tuple[int, int]] = [(x, y) for (x, y) in locations if x < half_height and y > half_width]
    right_up: List[Tuple[int, int]] = [(x, y) for (x, y) in locations if x > half_height and y < half_width]
    right_down: List[Tuple[int, int]] = [(x, y) for (x, y) in locations if x > half_height and y > half_width]
    return len(left_up), len(right_up), len(left_down), len(right_down)


def first_part():
    width: int = 101
    height: int = 103
    iterations: int = 100
    robots: List[Tuple[Tuple[int, int], Tuple[int, int]]] = get_robots()
    tmp = []
    for robot in robots:
        robot = location_after(robot=robot, iterations=iterations, width=width, height=height), robot[1]
        tmp.append(robot)
    robots = tmp
    left_up, right_up, left_down, right_down = count_in_quadrant(
        width=width, height=height, locations=get_robot_locations(robots=robots)
        )
    print("safety factor", left_up * right_up * left_down * right_down)


def second_part():
    width: int = 101
    height: int = 103
    iterations: int = 1
    robots: List[Tuple[Tuple[int, int], Tuple[int, int]]] = get_robots()
    while True:
        tmp = []
        for robot in robots:
            robot = location_after(robot=robot, iterations=1, width=width, height=height), robot[1]
            tmp.append(robot)
        robots = tmp
        if should_print_matrix(width=width, height=height, locations=get_robot_locations(robots=robots)):
            print_matrix(width=width, height=height, locations=get_robot_locations(robots=robots))
            break
        iterations +=1
    print("iteration", iterations)


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
