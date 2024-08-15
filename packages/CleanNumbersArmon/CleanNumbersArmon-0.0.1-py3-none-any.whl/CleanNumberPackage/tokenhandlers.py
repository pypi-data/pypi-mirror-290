from abc import ABC, abstractmethod
from tokenClass import type
from tokenClass import token
import tokenHandlerHelpers
import string

class baseHandler(ABC):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def can_handle(self, request):
        """Determine if the handler can handle the request."""
        pass

    @abstractmethod
    def handle(self, request):
        """Process the request if possible; otherwise, pass it to the next handler."""
        pass

class Number(baseHandler):
    def can_handle(self, request):
        if(len(request)<1):
            return False
        for item in request:
            if(item.type != type.number and item.type != type.other):
                return False
        return True

    def handle(self, request):
        if self.can_handle(request):
            evalstring = ""
            for token in request:
                evalstring += token.value
            evalstring = tokenHandlerHelpers.remove_leading_insignificant_digits(evalstring)
            result = eval(evalstring)
            return result
        elif self.next_handler:
            return self.next_handler.handle(request)

class Exponent_E(baseHandler):
    def can_handle(self, request):
        exponent_count = 0
        for token in request:
            if token.type == type.alpha:
                return False
            if token.type == type.exponent:
                exponent_count += 1
                # Early exit if more than one exponent token is found
                if exponent_count > 1:
                    return False
    # Check if exactly one exponent token was found
        return exponent_count == 1

    def handle(self, request):
        if self.can_handle(request):
            evalstr = ""
            for token in request:
                evalstr += token.value
            result = eval(tokenHandlerHelpers.convert_scientific_notation(evalstr))
            return result
        elif self.next_handler:
            return self.next_handler.handle(request)

class Operation(baseHandler):
    
   
    def can_handle(self, request):
        for token in request:
            if(token.type == type.carrot or token.type == type.operation):
                return True
        return False

    def handle(self, request):
        alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWBXYZ" #define custom alpha list
        if self.can_handle(request):
            evalstr=""
            for token in request:
                if token.value not in alpha:
                    evalstr += token.value
            if len(evalstr)>1: #handle edgecase where N/A makes it through, or "*"
                evalstr = evalstr.replace("^", "**")
                #if(evalstr.find("2**")):
                evalstr = evalstr.replace("(-00", "(-")
                evalstr = evalstr.replace("(-0", "(-")
                evalstr = evalstr.replace("(00", "(")
                evalstr = evalstr.replace("(0", "(")
                result = eval(evalstr)
                return result
            else:
                return "N/A"
            
        elif self.next_handler:
            return self.next_handler.handle(request)
            
class last_handler(baseHandler):
    def can_handle(self, request):
        return True
    
    def handle(self, request):
        str = ""
        for token in request: #handle edgecase of "1 foot"
            str += token.value
        if (str == "1foot"):
            return 1
        else:
            return "N/A"