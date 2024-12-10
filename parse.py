from collections import defaultdict

def calc_first(nt, grammar, n):
    der = []
    ff = set()
    for lhs, rhs in grammar.items():
        if lhs == nt:
            der = rhs
            break
    for production in der:
        if not production[0].isupper():
            ff.add(production[0])
        else:
            index = 0
            while index < len(production):
                eps = False
                der2 = calc_first(production[index], grammar, n)
                for x in der2:
                    if x == '#':
                        eps = True
                    else:
                        ff.add(x)
                if eps:
                    index += 1
                else:
                    break
    return ff

def calc_follow(nt, grammar, n):
    fl = set()
    if nt == list(grammar.keys())[0]:
        fl.add('$')
    for lhs, rhs_list in grammar.items():
        for production in rhs_list:
            for j, symbol in enumerate(production):
                if symbol == nt:
                    if j == len(production) - 1 and lhs != nt:
                        fl.update(calc_follow(lhs, grammar, n))
                    else:
                        if j + 1 < len(production):
                            next_symbol = production[j + 1]
                            if not next_symbol.isupper() and next_symbol != '#':
                                fl.add(next_symbol)
                            else:
                                index = j + 1
                                while index < len(production):
                                    eps = False
                                    der2 = calc_first(production[index], grammar, n)
                                    for x in der2:
                                        if x == '#':
                                            eps = True
                                        else:
                                            fl.add(x)
                                    if eps:
                                        index += 1
                                        if index == len(production):
                                            fl.update(calc_follow(lhs, grammar, n))
                                    else:
                                        break
    return fl

def build_parse_table(grammar, first, follow):
    parse_table = {}
    for nt, productions in grammar.items():
        for production in productions:
            if not production[0].isupper() and production[0] != '#':
                parse_table[(nt, production[0])] = production
            else:
                first_set = calc_first(production[0], grammar, len(grammar))
                for terminal in first_set:
                    if terminal != '#':
                        parse_table[(nt, terminal)] = production
                if '#' in first_set or production[0] == '#':
                    follow_set = calc_follow(nt, grammar, len(grammar))
                    for follow_symbol in follow_set:
                        if follow_symbol not in {' ', '\0'}:
                            parse_table[(nt, follow_symbol)] = "#"
    return parse_table

def parse_string(input_string, parse_table, start_symbol):
    stack = ['$']
    stack.append(start_symbol)
    i = 0
    while stack:
        top = stack[-1]
        current = input_string[i]
        if top == current:
            stack.pop()
            i += 1
        elif not top.isupper():
            return False
        elif (top, current) in parse_table:
            stack.pop()
            production = parse_table[(top, current)]
            if production != "#":
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            return False
    return i == len(input_string)

def main():
    n = int(input("Enter the number of lines in the grammar: "))
    grammar = defaultdict(list)
    print("Enter the grammar lines:")
    for _ in range(n):
        s = input().strip()
        lhs, rhs = s.split("->")
        productions = rhs.split("/")
        grammar[lhs.strip()] = [prod.strip() for prod in productions]
    first = {nt: calc_first(nt, grammar, n) for nt in grammar}
    follow = {nt: calc_follow(nt, grammar, n) for nt in grammar}
    print("\nFirst Sets:")
    for nt, first_set in first.items():
        print(f"First({nt}): {', '.join(sorted(first_set))}")
    print("\nFollow Sets:")
    for nt, follow_set in follow.items():
        print(f"Follow({nt}): {', '.join(sorted(follow_set))}")
    parse_table = build_parse_table(grammar, first, follow)
    print("\nPredictive Parse Table:")
    for key, value in parse_table.items():
        print(f"M[{key[0]}, {key[1]}] = {value}")
    input_string = input("Enter the string to parse (end with $): ").strip()
    if parse_string(input_string, parse_table, list(grammar.keys())[0]):
        print("The string is accepted by the grammar.")
    else:
        print("The string is rejected by the grammar.")

if _name_ == "_main_":
    main()
