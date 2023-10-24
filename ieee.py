def float_to_ieee_754(number, single_precision=True):
    if single_precision:
        bias = 127
        exponent_bits = 8
        significand_bits = 23
        total_bits = 32
    else:
        bias = 1023
        exponent_bits = 11
        significand_bits = 52
        total_bits = 64

    if number == 0:
        sign_bit = '0'
        exponent = '0' * exponent_bits
        significand = '0' * significand_bits
    else:
        sign_bit = '0' if number >= 0 else '1'
        number = abs(number)
        exponent = '0' * exponent_bits
        integer_part = int(number)
        fractional_part = number - integer_part

        # Convert the integer part to binary
        integer_binary = bin(integer_part)[2:]
        exponent_value = len(integer_binary) - 1 + bias

        # Convert the fractional part to binary
        fractional_binary = ''
        for _ in range(significand_bits):
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_binary += str(bit)
            fractional_part -= bit

        significand = integer_binary[1:] + fractional_binary

        # Ensure the significand has the correct length
        if len(significand) < significand_bits:
            significand = significand + '0' * (significand_bits - len(significand))
        else:
            significand = significand[:significand_bits]

        # Convert the exponent to binary and ensure it has the correct length
        exponent_binary = bin(exponent_value)[2:]
        exponent = '0' * (exponent_bits - len(exponent_binary)) + exponent_binary

    ieee_754 = sign_bit + exponent + significand

    if single_precision:
        N = (-1) ** int(sign_bit) * (1 + int(significand, 2) / (2 ** significand_bits)) * 2 ** (int(exponent, 2) - bias)
        Nx = hex(int(ieee_754, 2))[2:]
        return (ieee_754 + " | Exposant E = " + exponent + " | M = " + significand + " | S = " + sign_bit + " | N = -1^S x 1,M x 2^(E-" + str(bias) + ") = " + str(N) + " | N(16) = " + str(Nx))
    else:
        return ieee_754[:total_bits]



def ieee_754_to_float(N, base): # ieee-754 32 bits

    if base == 10:
        N = str(N)
        a = int(N[0])        # sign,     1 bit
        b = int(N[1:9], 2)   # exponent, 8 bits
        c = int("1" + N[9:], 2)  # fraction, len(N)-9 bits
    
        return (-1) ** a * c / (1 << (len(N) - 9 - (b - 127)))
    
    if base == 16:
        return hex(int(N,2))[2:]


def miniMenu(option):
    if option == 1:
        single_precision_binary = float_to_ieee_754(float(input("Ton nombre décimal : ")), single_precision=True)
        print("Single Precision (32 bits):", str(single_precision_binary))
    if option == 2:
        ieee = input("Ton ieee (32bits) : ")
        single_conversion_decimal = ieee_754_to_float(ieee, 10)
        single_conversion_hex = ieee_754_to_float(ieee, 16)
        print("Conversion decimal : " + str(single_conversion_decimal) + "  |  Conversion Hex : " + str(single_conversion_hex))

option = float(input('1 or 2   : '))
miniMenu(option)
