from typing import List, Optional, Set


def get_lines(string: str) -> list[str]:
    return string.split("\n")


def lines_of_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return get_lines(file.read())


def get_rules(lines: List[str]) -> dict[int, Set[int]]:
    rules: dict[int, Set[int]] = {}
    for line in lines:
        line: List[str] = line.split("|")
        before: int = int(line[0])
        after: int = int(line[1])
        if before not in rules:
            rules[before] = {after}
        else:
            rules[before].add(after)
    return rules


def get_updates(lines: List[str]) -> List[List[int]]:
    updates: List[List[int]] = []
    for line in lines:
        updates.append([int(c) for c in line.split(",")])
    return updates


def get_rules_and_updates() -> (dict[int, Set[int]], List[List[int]]):
    lines: List[str] = lines_of_file("first.txt")
    rule_lines: List[str] = []
    updates_lines: List[str] = []
    updates: bool = False
    for line in lines:
        if line == "":
            updates = True
            continue
        if updates:
            updates_lines.append(line)
        else:
            rule_lines.append(line)
    return get_rules(rule_lines), get_updates(updates_lines)


def first_part():
    (rules, updates) = get_rules_and_updates()

    valid: List[List[int]] = []
    for update in updates:
        if check_update(rules=rules, update=update):
            valid.append(update)
    print("sum", sum_up(valid))


def check_update(rules: dict[int, Set[int]], update: List[int]) -> bool:
    fine: bool = True
    for current_index, page in enumerate(update):
        if page not in rules:
            # no rules, no problem
            continue
        current_rule: Set[int] = rules[page]
        if not all([index > current_index for index, c in enumerate(update) if c in list(current_rule)]):
            fine = False
            break
    return fine


def replace_first_wrong_one(rules: dict[int, Set[int]], update: List[int]) -> Optional[List[int]]:
    if check_update(rules=rules, update=update):
        return update
    for current_index, page in enumerate(update):
        if page not in rules:
            # no rules, no problem
            continue
        current_rule: List[int] = list(rules[page])
        wrong_one = [(index > current_index, index, c) for index, c in enumerate(update) if c in list(current_rule)]
        if not all([a for (a, _, _) in wrong_one]):
            (index, number) = [(i, n) for (a, i, n) in wrong_one if not a][0]
            update[index] = page
            update[current_index] = number
            return replace_first_wrong_one(rules=rules, update=update)
    return None


def sum_up(valid: List[List[int]]) -> int:
    s: int = 0
    for update in valid:
        s += update[int((len(update) - 1) / 2)]
        # print(update)
    return s


def second_part():
    (rules, updates) = get_rules_and_updates()

    valid: List[List[int]] = []
    invalid: List[List[int]] = []
    for update in updates:
        current_update = update.copy()
        if check_update(rules=rules, update=update):
            valid.append(current_update)
        else:
            invalid.append(current_update)

    valid = []
    for update in invalid:
        tmp = replace_first_wrong_one(rules=rules, update=update)
        if tmp:
            valid.append(tmp)
    print("sum", sum_up(valid))


def main():
    first_part()
    second_part()


if __name__ == "__main__":
    main()
