from collections import defaultdict

def compute_first(rules, nonterms, terms):
    first = defaultdict(set)

    def get_first(symbol):
        if symbol in terms:  # If terminal, return itself
            return {symbol}
        if symbol in first:  # Already computed
            return first[symbol]

        result = set()
        for rhs in rules.get(symbol, []):
            if rhs == "#":  # Epsilon
                result.add("#")
            else:
                for char in rhs:
                    char_first = get_first(char)
                    result.update(char_first - {"#"})
                    if "#" not in char_first:
                        break
                else:
                    result.add("#")  # All nullable
        first[symbol] = result
        return result

    for nt in nonterms:
        get_first(nt)

    return first

def compute_follow(rules, nonterms, terms, first):
    follow = defaultdict(set)
    start = next(iter(nonterms))
    follow[start].add("$")  # Start symbol gets '$'

    while True:
        changed = False
        for lhs, rhs_list in rules.items():
            for rhs in rhs_list:
                for i in range(len(rhs)):
                    if rhs[i] in nonterms:
                        # Process symbols after the current non-terminal
                        for k in range(i + 1, len(rhs)):
                            if rhs[k] in terms:
                                if rhs[k] not in follow[rhs[i]]:
                                    follow[rhs[i]].add(rhs[k])
                                    changed = True
                                break
                            elif rhs[k] in nonterms:
                                add_set = first[rhs[k]] - {"#"}
                                if add_set - follow[rhs[i]]:
                                    follow[rhs[i]].update(add_set)
                                    changed = True
                                if "#" not in first[rhs[k]]:
                                    break
                        else:  # If no symbols left or all can be ε
                            if follow[lhs] - follow[rhs[i]]:
                                follow[rhs[i]].update(follow[lhs])
                                changed = True
        if not changed:
            break

    return follow


# Input and processing
n = int(input("Enter the number of rules: "))
rules = defaultdict(list)
nonterms = set()
terms = set()

print("Enter rules (use '#' for epsilon, e.g., A->aB|#):")
for _ in range(n):
    line = input().strip()
    lhs, rhs = line.split("->")
    nonterms.add(lhs)
    for option in rhs.split("|"):
        rules[lhs].append(option)
        for char in option:
            if not char.isupper() and char != "#":
                terms.add(char)

# Compute First and Follow sets
first = compute_first(rules, nonterms, terms)
follow = compute_follow(rules, nonterms, terms, first)

# Output results
print("\nFirst sets:")
for nt in nonterms:
    print(f"First({nt}) = {{ {', '.join(first[nt])} }}")

print("\nFollow sets:")
for nt in (nonterms):
    print(f"Follow({nt}) = {{ {', '.join((follow[nt]))} }}")
