
def replace_combined_numbers_with_spelling(string: str):
    combinations: list[list[str, str]] = [
        ["oneight", "oneeight"],
        ["twone", "twoone"],
        ["threeight", "threeeight"],
        ["fiveight", "fiveeight"],
        ["eighthree", "eightthree"],
        ["eightwo", "eighttwo"],
        ["eightwo", "eighttwo"],
        ["nineight", "nineeight"],
    ]
    for element in combinations:
        if element[0] in string:
            string = string.replace(element[0], element[1])
    return string

def replace_spelling_with_numbers(string: str):
    replacements: int = 1
    while replacements > 0:
        replacements = 0
        string = string.lower()
        string = replace_combined_numbers_with_spelling(string)
        tuples: list[list[str, str, int]] = [
            ["one", "1", -1],
            ["two", "2", -1],
            ["three", "3", -1],
            ["four", "4", -1],
            ["five", "5", -1],
            ["six", "6", -1],
            ["seven", "7", -1],
            ["eight", "8", -1],
            ["nine", "9", -1],
        ]
        for element in tuples:
            if element[0] in string:
                element[2] = string.index(element[0])
        tuples.sort(key=lambda x: x[2])
        for element in tuples:
            if element[2] != -1:
                if element[0] in string:
                    string = string.replace(element[0], element[1], 1)
                    replacements += 1
        for element in tuples:
            if element[2] != -1:
                if element[0] in string:
                    string = string.replace(element[0], element[1], 1)
                    replacements += 1
    return string


def main():
    value: str = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineightseven2
zoneight234
7pqrstsixteen
"""
    # with open("second_input.txt", "r") as file:
    #     value = file.read()
    numbers: list[list[str]] = []
    linearray: list[str] = []
    for line in value.split("\n"):
        line = replace_spelling_with_numbers(line)
        linearray.append(line)
        lineInput: list[str] = []
        for char in line:
            if char.isdigit():
                lineInput.append(char)
        if len(lineInput) > 0:
            numbers.append(lineInput)
    print(numbers)

    overall_sum: int = 0
    for i, line in enumerate(numbers):
        tens: int = 0
        ones: int = 0
        if len(line) >= 2:
            tens: int = int(line[0]) * 10
            ones: int = int(line[-1])
        elif len(line) == 1:
            tens: int = int(line[0]) * 10
            ones: int = int(line[0])
        print(f"{linearray[i]} -> {tens + ones}")
        overall_sum += tens + ones

    print(f"Overall sum: {overall_sum}")


if __name__ == '__main__':
    main()
