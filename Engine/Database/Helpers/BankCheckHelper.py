from Enums.ReturnValues import ReturnValues
from Model.BankCheck import BankCheck

class BankCheckHelper:
    def readAndDelete(self, cursor, code):
        cursor.execute("select * from bank_check where code = '{}'".format(code))
        bankCheckTuple = cursor.fetchone()
                        
        if bankCheckTuple is None:
            return ReturnValues.doesntExist
        else:
            cursor.execute("delete from bank_check where code = {}".format(code))                 
            return self.getObjectFromTuple(bankCheckTuple)

    def getObjectFromTuple(self, bankCheckTuple):
        return BankCheck(bankCheckTuple[0], bankCheckTuple[1], bankCheckTuple[2])