
class BankCheck:
    def __init__(self, code, currency, amount):   # currency je jedan od ovih stringova: "rsd", "eur", "usd"
        self.code = code
        self.currency = currency
        self.amount = amount        
        
    def __repr__(self):
        return f"BankCheck(code={self.code}, currency={self.currency}, amount={self.amount})"
