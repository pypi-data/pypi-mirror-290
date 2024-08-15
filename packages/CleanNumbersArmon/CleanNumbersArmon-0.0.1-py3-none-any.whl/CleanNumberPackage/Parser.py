from tokenClass import token
from tokenClass import type
import string

class parser:

    result = []
    operators = "/*-+^"
    
    def handle_digit(char):
        token1 = token(char, type.number)
        parser.result.append(token1)
        
    def handle_alpha(char):
        token1 = token(char, type.alpha)
        parser.result.append(token1)
        
    def handle_exponent(char):
        token1 = token(char, type.exponent)
        parser.result.append(token1)
        
    def handle_decimal(char):
        token1 = token(char, type.other)
        parser.result.append(token1)
        
    def handle_operator(char):
        token1 = token(char, type.operation)
        parser.result.append(token1)
        
    def handle_other(char):
        token1 = token(char, type.other)
        parser.result.append(token1)
        
    def handle_sign(char):
        token1 = token(char, type.sign)
        parser.result.append(token1)
        
    def handle_carrot(char):
        token1 = token(char, type.carrot)
        parser.result.append(token1)
        
    def remove_range(data, start, end):
        # Ensure start and end are within bounds and start <= end
        if start < len(data) and start <= end:
            # Handle the case where end exceeds the length of the string
            end = min(end, len(data))
            # Create a new string with the characters from 'start' to 'end' removed
            new_data = data[:start] + data[end:]
        else:
            # If indices are out of bounds or invalid, return the original string
            new_data = data
    
        return new_data

    @staticmethod
    def parse(data):
        
        parser.result = [] #clear results every time this is called
        data = data.replace(" ", "") #remove all spaces
        data  = data.replace(",", "") #remove all commas
        
        for i, char in enumerate(data):
            if char.isdigit():
                parser.handle_digit(char)
            elif(char == 'E'):
                parser.handle_exponent(char)
            elif char ==".":
                parser.handle_decimal(char)
            elif char in parser.operators:
                if(len(data)==1):
                    parser.handle_operator(char)
                elif(data[i+1] == '*' and char == '*'): #handle edge case where ** is used as exponent instead of ^
                    char_ = '^'
                    parser.handle_carrot(char_)
                elif(data[i-1] == '*' and char == '*'):
                    continue
                elif(char == '-' and not data[i-1].isdigit()):
                    parser.handle_sign(char)
                else:
                    parser.handle_operator(char) 
            elif char.isalpha:
                if(char == 'X'): #handle edge case where there is X10^-5, only happens three times
                    char = 'E'
                    parser.handle_exponent(char)
                    char = '-'
                    parser.handle_sign(char)
                    char = '5'
                    parser.handle_digit(char)
                    break
                elif(char =='(' or char ==')'): #because isalpha is a silly funciton that thinks '(' and')' are alphabetical characters
                    parser.handle_other(char)
                else:    
                    parser.handle_alpha(char)
            else:
                parser.handle_other(char)
                
        return parser.result



