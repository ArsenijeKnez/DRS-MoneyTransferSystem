
class CardAndBalanceOfUserDTO:
    def __init__(self, number=None, exp_date=None, cvc=None, verified=None, currency=None, amount=None):
        self.number = number
        self.exp_date = exp_date
        self.cvc = cvc
        self.verified = verified
        self.currency = currency
        self.amount = amount
        
    def getObjectListFromTupleList(self, tupleList):
        objectList = []
        
        for tuple in tupleList:
            objectList.append(CardAndBalanceOfUserDTO(number=tuple[0], exp_date=tuple[1], cvc=tuple[2], verified=tuple[3], currency=tuple[4], amount=tuple[5]))

        return objectList

    def __repr__(self):
        return f"CardAndBalanceOfUserDTO(number={self.number}, exp_date={self.exp_date}, cvc={self.cvc}, verified={self.verified}, currency={self.currency}, amount={self.amount})"
