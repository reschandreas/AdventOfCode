from typing import List, Tuple, Optional


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_input() -> str:
    return lines_of_file('first.txt')[0]


def visualize(tagged: List[Tuple[str, int, bool]]) -> str:
    line: str = ''
    for value, c, empty in tagged:
        for i in range(c):
            if empty:
                line += '.'
            else:
                line += str((value))
                # line += str(ord(value))
    # print(line)
    return line


def to_array(tagged: List[Tuple[str, int, bool]]) -> List[Optional[str]]:
    line: List[Optional[str]] = []
    for value, c, empty in tagged:
        for i in range(c):
            if empty:
                line.append(None)
            else:
                line.append(value)
    return line


def tag_line(line: str) -> List[Tuple[str, int, bool]]:
    tagged: List[Tuple[str, int, bool]] = []
    counter: int = 0
    for index, c in enumerate(line):
        even: bool = index % 2 == 1
        tagged.append((counter, int(c), index % 2 == 1))
        # tagged.append((chr(counter), int(c), index % 2 == 1))
        if even:
            counter += 1
    return tagged


def compress(tagged: List[Tuple[str, int, bool]]):
    line: List[str] = to_array(tagged=tagged)
    start: int = 0
    end: int = len(line) - 1
    while start < end:
        a: str = line[start]
        if a is None:
            b: str = line[end]
            if b is not None:
                line[start] = b
                line[end] = a
                end -= 1
                start += 1
            else:
                end -= 1
        else:
            start += 1
    return line


def move_block(tagged: List[Tuple[str, int, bool]], start: int, end: int) -> List[Tuple[str, int, bool]]:
    moveable_block = tagged[end]
    if moveable_block[2]:
        return tagged
    while start < end:
        avalue, alen, afree = tagged[start]
        if afree:
            bvalue, blen, bfree = tagged[end]
            if not bfree and blen <= alen:
                tagged[start] = (bvalue, blen, bfree)
                tagged[end] = (0, blen, True)
                tagged.insert(start + 1, (avalue, alen - blen, afree))
                return tagged
            else:
                start += 1
        else:
            start += 1
    return tagged


def compress_whole_blocks(tagged: List[Tuple[str, int, bool]]):
    start: int = 0
    end: int = len(tagged) - 1
    while start < end:
        avalue, alen, afree = tagged[start]
        if afree:
            tagged = move_block(tagged=tagged, start=0, end=end)
            end -= 1
        else:
            start += 1
    return to_array(tagged=tagged)


def calculate_checksum(line: List[str]) -> int:
    checksum: int = 0
    for i, c in enumerate(line):
        if c is not None:
            # checksum += ord(c) * i
            checksum += c * i
    return checksum


def first_part():
    line: str = get_input()
    tagged = tag_line(line)
    # print(visualize(tagged=tagged))
    line: List[str] = compress(tagged=tagged)
    checksum: int = calculate_checksum(line)
    print("checksum", checksum)


def second_part():
    line: str = get_input()
    tagged = tag_line(line)
    line: List[str] = compress_whole_blocks(tagged=tagged)
    checksum: int = calculate_checksum(line)
    print("checksum", checksum)


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
