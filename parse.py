# Function to eliminate left recursion
def eliminate_left_recursion(productions):
    new_productions = {}
    for nt, rhs in productions.items():
        alpha = []
        beta = []
        for production in rhs:
            if production.startswith(nt):
                alpha.append(production[len(nt):])
            else:
                beta.append(production)
        
        if alpha:
            new_nt = nt + "'"
            new_productions[nt] = [b + new_nt for b in beta]
            new_productions[new_nt] = [a + new_nt for a in alpha] + ['∈']
        else:
            new_productions[nt] = rhs
    
    return new_productions

# Function to find the longest common prefix (for left factoring)
def longest_common_prefix(strings):
    if not strings:
        return ""
    
    prefix = strings[0]
    for string in strings[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

# Function for left factoring
def left_factoring(productions):
    factored_productions = {}
    for nt, rhs_list in productions.items():
        common_prefix = longest_common_prefix(rhs_list)
        
        if common_prefix:
            new_rhs = [rhs[len(common_prefix):] for rhs in rhs_list if rhs.startswith(common_prefix)]
            new_nt = nt + "'"
            factored_productions[nt] = [common_prefix + new_nt]
            factored_productions[new_nt] = new_rhs + ['∈']
        else:
            factored_productions[nt] = rhs_list
    
    return factored_productions

# Function to calculate First set
def calc_first(nt, productions, first_sets):
    if nt in first_sets:
        return first_sets[nt]
    
    first = set()
    rhs = productions[nt]
    for production in rhs:
        if not production[0].isupper():
            first.add(production[0])
        else:
            for symbol in production:
                if symbol.isupper():
                    symbol_first = calc_first(symbol, productions, first_sets)
                    first.update(symbol_first - {'∈'})
                    if '∈' not in symbol_first:
                        break
                else:
                    first.add(symbol)
                    break
    first_sets[nt] = first
    return first

# Function to calculate Follow set
def calc_follow(nt, productions, first_sets, follow_sets, start_symbol):
    if nt in follow_sets:
        return follow_sets[nt]
    
    follow = set()
    if nt == start_symbol:
        follow.add('$')
    
    for lhs, rhs_list in productions.items():
        for rhs in rhs_list:
            for i in range(len(rhs)):
                if rhs[i] == nt:
                    if i + 1 < len(rhs):
                        next_symbol = rhs[i + 1]
                        if next_symbol.isupper():
                            follow.update(first_sets[next_symbol] - {'∈'})
                            if '∈' in first_sets[next_symbol]:
                                follow.update(calc_follow(lhs, productions, first_sets, follow_sets, start_symbol))
                        else:
                            follow.add(next_symbol)
                    else:
                        follow.update(calc_follow(lhs, productions, first_sets, follow_sets, start_symbol))
    
    follow_sets[nt] = follow
    return follow

# Function to build the predictive parsing table
def build_parse_table(productions, first_sets, follow_sets):
    parse_table = {}
    for nt, rhs_list in productions.items():
        for production in rhs_list:
            if production == '∈':
                for symbol in follow_sets[nt]:
                    parse_table[(nt, symbol)] = production
            else:
                for symbol in first_sets[nt]:
                    parse_table[(nt, symbol)] = production
    return parse_table

# Function to parse a string using the predictive parsing table
def parse_string(input_string, parse_table, start_symbol):
    stack = ['$']
    stack.append(start_symbol)
    input_string += '$'
    i = 0

    while len(stack) > 0:
        top = stack.pop()
        current = input_string[i]

        if top == current:
            i += 1
        elif not top.isupper():
            return False
        elif (top, current) in parse_table:
            production = parse_table[(top, current)]
            if production != '∈':
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            return False
    
    return True

# Main Function (as per the console format given in the picture)
def run_grammar_processing():
    # Input grammar
    n = int(input("Enter the number of lines in the grammar: "))
    productions = {}
    print("Enter the different lines of grammar:")
    for _ in range(n):
        line = input().strip()
        lhs, rhs = line.split("→")
        productions[lhs.strip()] = [x.strip() for x in rhs.split('|')]

    # Step 1: Eliminate Left Recursion
    productions = eliminate_left_recursion(productions)

    # Step 2: Left Factoring
    productions = left_factoring(productions)

    # Step 3: Calculate First and Follow sets
    first_sets = {}
    follow_sets = {}
    start_symbol = list(productions.keys())[0]

    for nt in productions:
        calc_first(nt, productions, first_sets)
    for nt in productions:
        calc_follow(nt, productions, first_sets, follow_sets, start_symbol)

    # Display First sets
    for nt, first in first_sets.items():
        print(f"First of {nt} {{{','.join(first)}}}")

    # Display Follow sets
    for nt, follow in follow_sets.items():
        print(f"Follow of {nt} {{{','.join(follow)}}}")

    # Step 4: Build Predictive Parsing Table
    parse_table = build_parse_table(productions, first_sets, follow_sets)

    # Display Predictive Parsing Table
    print("Predictive Parsing Table:")
    for (nt, terminal), production in parse_table.items():
        print(f"M[{nt}, {terminal}] = {production}")

    # Step 5: Parse Input String
    input_string = input("Enter the string to parse (end with $): ").strip()
    if parse_string(input_string, parse_table, start_symbol):
        print("The string is accepted by the grammar.")
    else:
        print("The string is rejected by the grammar.")

# Run the main function
run_grammar_processing()
