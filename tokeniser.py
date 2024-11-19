import re
keywords = ["int", "float", "if", "while", "return"]
a_operators = ["+", "-", "*", "/", "%"]
l_operators = ["&&", "||", "!"]
o_operators = ["=", "+=", "-=", "*=", "/=", "%="]
delimiters = [",", ":", ";", "(", ")", "{", "}", "[", "]"]
comments = []
preprocessor_directives = []
identifiers = []
constants = []
key = []
aops = []
lops = []
oops = []
delims = []
file_name = input("Enter the name of the C file to generate tokens: ")
with open(file_name, 'r') as file:
    lines = file.readlines()
for line in lines:
    line = line.strip()
    if line.startswith("#"):
        preprocessor_directives.append(line)
        continue
    if line.startswith("//") or line.startswith("/*"):
        comments.append(line)
        continue
    words = re.split(r'(\W)', line)
    for word in words:
        word = word.strip()
        if word == "":
            continue
        if word in keywords:
            key.append(word)
        elif word in a_operators:
            aops.append(word)
        elif word in l_operators:
            lops.append(word)
        elif word in o_operators:
            oops.append(word)
        elif word in delimiters:
            delims.append(word)
        elif word.isdigit():
            constants.append(word)
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', word):
            if word not in keywords and word not in identifiers:
                identifiers.append(word)
print("\nKeywords:")
print(key)
print("\nIdentifiers (Variable Names):")
print(identifiers)
print("\nArithmetic Operators:")
print(aops)
print("\nLogical Operators:")
print(lops)
print("\nOther Operators:")
print(oops)
print("\nDelimiters:")
print(delims)
print("\nConstants:")
print(constants)
print("\nComments:")
print(comments)
print("\nPreprocessor Directives:")
print(preprocessor_directives)
