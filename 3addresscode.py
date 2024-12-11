def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def infix_to_postfix(expr):
    operators = []
    postfix = []
    for ch in expr:
        if ch.isspace():
            continue
        if ch.isalnum():  # Operand (numbers or variables)
            postfix.append(ch)
        elif ch == '(':
            operators.append(ch)
        elif ch == ')':
            while operators and operators[-1] != '(':
                postfix.append(operators.pop())
            operators.pop()  # Remove '('
        else:  # Operator
            while operators and precedence(operators[-1]) >= precedence(ch):
                postfix.append(operators.pop())
            operators.append(ch)
    
    # Pop remaining operators
    while operators:
        postfix.append(operators.pop())
    return ''.join(postfix)

def generate_temp(tc):
    temp = f"T{tc}"
    tc += 1
    return temp, tc

def generate_tac(expr):
    s = []
    code = []
    tc = 1
    for ch in expr:
        if ch in '+-*/':  # Operator
            op1 = s.pop()
            op2 = s.pop()
            temp, tc = generate_temp(tc)
            instruction = f"{temp} := {op2} {ch} {op1}"
            code.append(instruction)
            s.append(temp)
        else:  # Operand (variable or number)
            s.append(ch)
    
    # Final result
    if s:
        result = s.pop()
        code.append(f"Result := {result}")
    
    print("The intermediate code:")
    for line in code:
        print(line)

# Main program
expr = input("Enter the Expression: ")
postfix_expr = infix_to_postfix(expr)  # Directly convert infix to postfix
generate_tac(postfix_expr)
