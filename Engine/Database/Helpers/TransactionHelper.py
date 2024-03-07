from Database.Helpers.TransactionIdHelper import TransactionIdHelper
from Model.Transaction import Transaction

class TransactionHelper:
    def getObjectListFromTupleList(self, transactionTupleList):
        transactions = []
        for transactionTuple in transactionTupleList:
            transactions.append(Transaction(transactionTuple[0], transactionTuple[1], transactionTuple[2], transactionTuple[3], transactionTuple[4], transactionTuple[5], transactionTuple[6]))

        return transactions

    def readIdOfUnexecuted(self, cursor, senderCardNum, receiverCardNum):
        cursor.execute("select transaction_id from transaction where executed = 0 and sender_card_num = '{senderCardNum}' and receiver_card_num = '{receiverCardNum}'".format(senderCardNum = senderCardNum, receiverCardNum = receiverCardNum))
        return cursor.fetchone()[0]

    def readUnexecutedTransactions(self, cursor):
        cursor.execute("select * from transaction where executed = 0")
        return self.getObjectListFromTupleList(cursor.fetchall())

    def readLastExecuted(self, cursor, numberOfTransactions):
        cursor.execute("select * from transaction where executed = 1 order by date_and_time desc limit {}".format(numberOfTransactions))
        return self.getObjectListFromTupleList(cursor.fetchall())
    
    def deleteUnexecuted(self, cursor, senderCardNum, receiverCardNum):
        # Posto sam stavio "on delete cascade", samo treba da obrisem iz transaction_id tabele i onda se automatski obrise i iz transaction tabele
        transactionIdHelper = TransactionIdHelper()
        transactionIdHelper.delete(cursor, self.readIdOfUnexecuted(cursor, senderCardNum, receiverCardNum))
                
    def setExecutedTo1(self, cursor, senderCardNum, receiverCardNum):
        cursor.execute("update transaction set executed = 1 where executed = 0 and sender_card_num = '{senderCardNum}' and receiver_card_num = '{receiverCardNum}'".format(senderCardNum = senderCardNum, receiverCardNum = receiverCardNum))

    def unexecutedExists(self, cursor, senderCardNum, receiverCardNum):
        cursor.execute("select count(*) from transaction where executed = 0 and sender_card_num = '{senderCardNum}' and receiver_card_num = '{receiverCardNum}'".format(senderCardNum = senderCardNum, receiverCardNum = receiverCardNum))
                    
        if cursor.fetchone()[0] == 0:
            return False
        else:
            return True 