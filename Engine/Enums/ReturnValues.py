
from enum import Enum

class ReturnValues(Enum):
    exception = -1
    
    alreadyExists = -11
    doesntExist = -12
    unexecutedTransactionAlreadyExists = -13
    
    insufficientFunds = -21
    cardNotVerified = -22
    
    emailInvalid = -31
    firstNameInvalid = -32
    lastNameInvalid = -33
    
