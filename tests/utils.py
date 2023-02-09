import decimal

def convert_to_string(number):
    number = decimal.Decimal(number) # Creating Decimal Instance from Number(12.1231e-09)
    digit = abs(number.as_tuple().exponent) # Getting the precision count // If 0.123123 -> output will be 6
    number_str = f"{float(number):.{digit}f}" # returning with specific precision
    number_str = number_str.replace('.', '')
    return number_str