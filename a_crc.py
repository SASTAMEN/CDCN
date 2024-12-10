def polynomial_to_binary(polynomial):
    """
    Convert a polynomial representation like x4+x2+1 to a binary string.
    """
    terms = polynomial.split('+')
    print(terms)
    max_power = int(terms[0][1:])  # Extract the highest power
    binary = ['0'] * (max_power + 1)

    for term in terms:
        if len(term)==1:
            #in this case there wont be anything next to x 
            #so we cant do x[1:]
            if term=='x':
                power=1
            elif term=='1':
                power=0
        else:
            power=int(term[1:])
        binary[-(power + 1)] = '1'
    print(binary)
    return ''.join(binary)

def calculate_crc(message, key):
    message = list(map(int, message))
    key = list(map(int, key))
    for i in range(len(message) - len(key) + 1):
        if message[i] == 1:
            for j in range(len(key)):
                #storing the xor values in msg only
                message[i + j] ^= key[j]
    print(message)
    remainder = message[(len(message) - len(key)+1):]
    print("rem",remainder)
    return ''.join(map(str, remainder))


def sender_side(data, key):
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = calculate_crc(appended_data, key)
    codeword = data + remainder
    print("=== Sender Side ===")
    print("Input Data:", data)
    print("Generator Polynomial (Binary):", key)
    print("CRC:", remainder)
    print("Codeword (Data + CRC):", codeword)
    return codeword

def receiver_side(codeword, key):
    remainder = calculate_crc(codeword, key)
    print("\n=== Receiver Side ===")
    print("Received Codeword:", codeword)
    print("Generator Polynomial (Binary):", key)
    print("Syndrome (Remainder):", remainder)
    if remainder == '0' *(len(key)-1):
        print("Result: No Error in transmission.")
    else:
        print("Result: Error detected in transmission.")

# Example usage
data = '1001'
polynomial = 'x8+x2+x+1'

# Convert polynomial to binary key
key = polynomial_to_binary(polynomial)

# Sender Side
codeword = sender_side(data, key)
print("code",codeword)

print('---------------')

# Receiver Side
receiver_side(codeword, key)
