
class TransactionWithUserDataDTO:
    def __init__(self, transaction, sender, receiver):
        self.transaction = transaction
        self.sender = sender
        self.receiver = receiver
        
    def __repr__(self):
        return f"TransactionWithUserDataDTO(transaction={self.transaction}, sender={self.sender}, receiver={self.receiver})"