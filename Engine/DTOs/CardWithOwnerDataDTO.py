
class CardWithOwnerDataDTO:
    def __init__(self, email=None, firstName=None, lastName=None, number=None, expDate=None, cvc=None):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.number = number
        self.expDate = expDate
        self.cvc = cvc
    
    def getObjectListFromTupleList(self, tupleList):
        objectList = []
        for tuple in tupleList:
            objectList.append(CardWithOwnerDataDTO(email=tuple[0], firstName=tuple[1], lastName=tuple[2], number=tuple[3], expDate=tuple[4], cvc=tuple[5]))
        
        return objectList

    def __repr__(self):
        return f"CardWithOwnerDataDTO(email={self.email}, firstName={self.firstName}, lastName={self.lastName}, number={self.number}, expDate={self.expDate}, cvc={self.cvc})"
