

def get_lines(string: str) -> list[str]:
    return string.split("\n")

def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())