def polynomial_to_binary(poly):
    """
    Convert a polynomial like x4+x2+1 to a binary string.
    """
    terms = poly.split('+')
    max_power = int(terms[0][1:])
    binary = ['0'] * (max_power + 1)

    for term in terms:
        if term == '1':
            binary[-1] = '1'
        else:
            power = int(term[1:])
            binary[-(power + 1)] = '1'
    
    return ''.join(binary)

def calculate_remainder(data, generator):
    data = list(map(int, data))
    generator = list(map(int, generator))
    for i in range(len(data) - len(generator) + 1):
        if data[i] == 1:
            for j in range(len(generator)):
                data[i + j] ^= generator[j]
    return ''.join(map(str, data[-(len(generator) - 1):]))

def send(data, generator):
    padded_data = data + '0' * (len(generator) - 1)
    crc = calculate_remainder(padded_data, generator)
    codeword = data + crc
    print("=== Sender ===")
    print("Data:", data)
    print("Generator:", generator)
    print("CRC:", crc)
    print("Codeword:", codeword)
    return codeword

def receive(codeword, generator):
    remainder = calculate_remainder(codeword, generator)
    print("\n=== Receiver ===")
    print("Codeword:", codeword)
    print("Generator:", generator)
    print("Remainder:", remainder)
    if remainder == '0' * (len(generator) - 1):
        print("Result: No error.")
    else:
        print("Result: Error detected.")

# Example usage
data = '100100'
polynomial = 'x4+x2+1'

# Convert polynomial to binary generator
generator = polynomial_to_binary(polynomial)

# Sender Side
codeword = send(data, generator)

print('---------------')

# Receiver Side
receive(codeword, generator)
