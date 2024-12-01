from typing import List

def get_lines(string: str) -> list[str]:
    return string.split("\n")

def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())

def first_part():
    lines = lines_of_file("first.txt")
    first: List[int] = []
    second: List[int] = []
    for line in lines:
        numbers: List[str] = line.split("   ")
        first.append(int(numbers[0]))
        second.append(int(numbers[1]))

    first.sort()
    second.sort()

    differences: List[int] = []
    sum: int = 0
    for i, f in enumerate(first):
        tmp = second[i] - f
        sum += abs(tmp)
        differences.append(tmp)


    print(sum)

def second_part():
    lines = lines_of_file("first.txt")
    first: List[int] = []
    count: dict[int, int] = {}
    for line in lines:
        numbers: List[str] = line.split("   ")
        first.append(int(numbers[0]))
        second_number = int(numbers[1])
        if second_number in count:
            count[second_number] = count.get(second_number) + 1
        else:
            count[second_number] = 1

    similarity: int = 0
    for number in first:
        tmp = number * count.get(number, 0)
        similarity += tmp
    print(similarity)


def main():
    # first_part()
    second_part()

if __name__ == '__main__':
    main()