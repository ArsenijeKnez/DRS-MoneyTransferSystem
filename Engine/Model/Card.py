
class Card:
    def __init__(self, number, expDate, cvc, ownerEmail, verified):
        self.number = number
        self.expDate = expDate
        self.cvc = cvc
        self.ownerEmail = ownerEmail
        self.verified = verified 
        
    def __repr__(self):
        return f"Card(number={self.number}, expDate={self.expDate}, cvc={self.cvc}, ownerEmail={self.ownerEmail}, verified={self.verified})"
