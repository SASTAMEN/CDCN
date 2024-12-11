import re

class ASTNode:
    def generate_code(self):
        raise NotImplementedError("Subclasses should implement this!")

class VariableNode(ASTNode):
    def _init_(self, name):
        self.name = name

    def generate_code(self):
        return f"LOAD {self.name}"

class ConstantNode(ASTNode):
    def _init_(self, value):
        self.value = value

    def generate_code(self):
        # Load the constant's value
        return f"LOAD {self.value}"

class BinaryOpNode(ASTNode):
    def _init_(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def generate_code(self):
        left_code = self.left.generate_code()
        right_code = self.right.generate_code()
        result = f"{left_code}\nSTORE TEMP\n{right_code}\nLOAD TEMP\n"
       
        if self.operator == "+":
            result += "ADD"
        elif self.operator == "*":
            result += "MUL"
        elif self.operator == "-":
            result += "SUB"
        elif self.operator == "/":
            result += "DIV"
       
        return result

class AssignNode(ASTNode):
    def _init_(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def generate_code(self):
        expression_code = self.expression.generate_code()
        return f"{expression_code}\nSTORE {self.variable.name}"

def tokenize(expression: str):
    tokens = re.findall(r'[a-zA-Z]+|\d+|[+\-*/=()]', expression.replace(" ", ""))
    return tokens

# Function to parse a variable or constant
def parse_factor(tokens):
    token = tokens.pop(0)
   
    if token.isdigit():  # If it's a number
        return ConstantNode(int(token))
    elif re.match(r'[a-zA-Z]+', token):  # If it's a variable
        return VariableNode(token)
    else:
        raise ValueError(f"Unexpected token in factor: {token}")

def parse_term(tokens):
    node = parse_factor(tokens)
   
    while tokens and tokens[0] in "*/":
        operator = tokens.pop(0)
        right = parse_factor(tokens)
        node = BinaryOpNode(operator, node, right)
   
    return node

# Function to parse an expression (which handles addition and subtraction)
def parse_expression(tokens):
    node = parse_term(tokens)
   
    while tokens and tokens[0] in "+-":
        operator = tokens.pop(0)
        right = parse_term(tokens)
        node = BinaryOpNode(operator, node, right)
   
    return node

def parse_assignment(tokens):
    variable = VariableNode(tokens.pop(0))  
    tokens.pop(0)  
    expression = parse_expression(tokens)
    return AssignNode(variable, expression)
def parse_statement(expression):
    tokens = tokenize(expression)
    return parse_assignment(tokens)
def generate_machine_code(ast: ASTNode) -> str:
    return ast.generate_code()

if _name_ == "_main_":
    expression = input("Enter an expression (e.g., a = b + c * d): ")
    ast = parse_statement(expression)
    machine_code = generate_machine_code(ast)
    print("Generated machine code:")
    print(machine_code)
