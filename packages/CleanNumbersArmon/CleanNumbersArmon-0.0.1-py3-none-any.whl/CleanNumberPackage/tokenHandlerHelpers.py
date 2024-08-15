import re
def to_floating_point_scientific(value):
    try:
        return format(float(value), ".14e")
    except ValueError:
        raise ValueError(f"Cannot convert {value} to a floating-point number.")
    
def remove_leading_insignificant_digits(number_str):
    """
    Remove leading insignificant digits from a string with numbers and decimals.
    """
    # Remove leading zeros in the integer part of the number
    # The regex pattern captures integer and decimal parts separately
    # It handles cases like '00123.456', '000.123', '000.000', and '123.000'
    match = re.match(r'^0*(\d+)(\.\d*)?', number_str)
    
    if match:
        # Combine integer and decimal parts, if present
        integer_part = match.group(1)
        decimal_part = match.group(2) or ''
        
        # Remove trailing zeros from the decimal part
        decimal_part = decimal_part.rstrip('0')
        
        # Construct the final result
        if decimal_part:
            # If there's a decimal part, add it back to the integer part
            return f"{integer_part}{decimal_part}"
        else:
            # If there's no decimal part left, just return the integer part
            return integer_part
    else:
        # If no match is found, return the original string
        return number_str

def convert_scientific_notation(number_str):
    """
    Convert scientific notation in a string to a more explicit form with *10**,
    handling optional leading zeros between E/e and the exponent, including negative exponents.
    """
    # Regex pattern to match scientific notation with optional leading zeros in the exponent
    pattern = re.compile(r'([0-9.]+)[Ee]([+-]?)0*(\d*)')
    
    def replacement(match):
        base = match.group(1)
        sign = match.group(2)
        exponent = match.group(3)
        if not exponent:
            exponent = '0'
        return f"{base}*10**{sign}{exponent}"
    
    # Replace occurrences of scientific notation in the string
    converted_str = pattern.sub(replacement, number_str)
    
    return converted_str



def clean_exponent(request):
        # Regex to match the pattern 2**(-07) and similar
        pattern = r'(\d+\*\*\(-0?)(\d+)\)'
        
        # Replace leading zeros in the exponent part
        def replace_leading_zero(match):
            base = match.group(1)
            exponent = match.group(2).lstrip('0')  # Remove leading zeros from exponent
            if exponent == '':
                exponent = '0'  # Handle case where exponent is all zeros
            return f"{base}{exponent})"
        
        return re.sub(pattern, replace_leading_zero, request)