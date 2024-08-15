
# Package metadata
__version__ = '0.1'
__author__ = 'Armon Barakchi'
__email__ = 'armon.barakchi@boeing.com'

#import for convenience
from CleanNumberPackage.CleanNumberPackage.tokenHandlerHelpers import to_floating_point_scientific
import tokenhandlers
import Parser
import tokenHandlerHelpers


#limit visibility
__all__ = ['tokenhandlers', 'Parser']

#define interface
def clean_number(value):
    
    #set up chain of command handlers
    handlerA = tokenhandlers.Number()
    handlerB = tokenhandlers.Exponent_E()
    handlerC = tokenhandlers.Operation()
    handlerD = tokenhandlers.last_handler()
    handlerA.set_next(handlerB).set_next(handlerC).set_next(handlerD)
    
    token_vector = Parser.parser.parse(value)
    result = handlerA.handle(item)
    result = str(to_floating_point_scientific(result))
    return result
    