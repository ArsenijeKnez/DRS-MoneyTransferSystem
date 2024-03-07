from datetime import datetime
from Utils.DateAndTimeParser import DateAndTimeParser

class Transaction:
    def __init__(self, transactionId, senderCardNum, receiverCardNum, currency, sentAmount, dateAndTime, executed):
        self.transactionId = transactionId
        self.senderCardNum = senderCardNum
        self.receiverCardNum = receiverCardNum
        self.currency = currency   # currency je jedan od ovih stringova: "rsd", "eur", "usd"
        self.sentAmount = sentAmount
        
        if not isinstance(dateAndTime, datetime):   # kada se pravi Transaction objekat od torke iz baze
            dateAndTimeParser = DateAndTimeParser()
            self.dateAndTime = dateAndTimeParser.parse(dateAndTime)
        else:   
            self.dateAndTime = dateAndTime
        
        self.executed = executed
        
    def __repr__(self):
        return f"Transaction(transactionId={self.transactionId}, senderCardNum={self.senderCardNum}, receiverCardNum={self.receiverCardNum}, currency={self.currency}, sentAmount={self.sentAmount}, dateAndTime={self.dateAndTime}, executed={self.executed})"
    def to_dict(self):
        return {
            "transactionId": self.transactionId,
            "senderCardNum": self.senderCardNum,
            "receiverCardNum": self.receiverCardNum,
            "currency": self.currency,
            "sentAmount": str(self.sentAmount),  # Convert Decimal to string
            "dateAndTime": self.dateAndTime.strftime("%Y-%m-%d %H:%M:%S"),  # Convert datetime to string
            "executed": self.executed
        }
