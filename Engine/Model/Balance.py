
class Balance:
    def __init__(self, cardNum, currency, amount):  # currency je jedan od ovih stringova: "rsd", "eur", "usd"
        self.cardNum = cardNum
        self.currency = currency
        self.amount = amount
        
    def __repr__(self):
        return f"Balance(cardNum={self.cardNum}, currency={self.currency}, amount={self.amount})"
