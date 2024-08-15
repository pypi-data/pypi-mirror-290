#types: number, exponent, operation, carrot(^), sign, alpha, other

from enum import Enum
import copy

class token:
    def __init__(self, aValue, aType):
       self.value = aValue 
       self.type = aType
        
    def __str__(self): #for debugging
        return f"Token(value={self.value}, type={self.type})"

    def __repr__(self): #for debugging
        return f"token(value={self.value!r}, type={self.type!r})"
        
    def __eq__(self, other): #define equality operator for unit tests
       if not isinstance(other, token):
           return False
       if(self.value == other.value and self.type == other.type):
           return True
       else:
           return False
       
    def copy(self):
        # Create a deep copy of the instance
        return copy.deepcopy(self)


class type(Enum):
    number = 1
    exponent = 2
    operation = 3
    carrot = 4
    sign = 5
    alpha = 6
    other =7

