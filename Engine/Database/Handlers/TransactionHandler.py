from Database.Handlers.UserHandler import UserHandler
from mysql.connector import connect
from datetime import datetime
from Database.Helpers.BalanceHelper import BalanceHelper
from Database.Helpers.CardHelper import CardHelper
from Database.Helpers.TransactionHelper import TransactionHelper
from Database.Helpers.TransactionIdHelper import TransactionIdHelper
from Enums.ReturnValues import ReturnValues
from Model.Transaction import Transaction

class TransactionHandler:
    transactionHelper = TransactionHelper()    

    # Doda novu transakciju u bazu. Poziva se kada korisnik zatrazi da se izvrsi transakcija. 
    # Povratne vrijednosti:
    #   ReturnValues.doesntExist - Kartica receiver-a ne postoji ili nije verifikovana
    #   ReturnValues.unexecutedTransactionAlreadyExists - Vec postoji jedna transakcija na cekanju kod koje je senderCardNum i receiverCardNum isti kao kod ove
    #   ReturnValues.insufficientFunds - Sender nema dovoljno novca
    #   ReturnValues.cardNotVerified - Kartica sender-a nije verifikovana
    def insert(self, senderCardNum, receiverCardNum, currency, sentAmount, receiverEmail, receiverFirstName, receiverLastName): 
        try:
            cardHelper = CardHelper()
            balanceHelper = BalanceHelper()       
            userHandler = UserHandler()
            
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    try:    
                        if not cardHelper.exists(cursor, receiverCardNum) or not cardHelper.verified(cursor, receiverCardNum):
                            return ReturnValues.doesntExist
                        
                        if self.transactionHelper.unexecutedExists(cursor, senderCardNum, receiverCardNum):
                            return ReturnValues.unexecutedTransactionAlreadyExists
                       
                        if not balanceHelper.amountGreaterOrEqualThan(cursor, senderCardNum, currency, sentAmount):
                            return ReturnValues.insufficientFunds
                        
                        if not cardHelper.verified(cursor, senderCardNum):
                            return ReturnValues.cardNotVerified
                        
                        ownerEmail = cardHelper.readOwnerEmail(receiverCardNum)
                        receiver = userHandler.read(ownerEmail)
                        if (receiver.email != receiverEmail):
                            return ReturnValues.emailInvalid
                        if (receiver.firstName != receiverFirstName):
                            return ReturnValues.firstNameInvalid
                        if (receiver.lastName != receiverLastName):
                            return ReturnValues.lastNameInvalid
        
                        transactionIdHelper = TransactionIdHelper()
                        transactionId = transactionIdHelper.readAndInsertFirstAvailable(cursor)
                            
                        cursor.execute("insert into transaction values ({transactionId}, '{senderCardNum}', '{receiverCardNum}', '{currency}', '{sentAmount}', '{dateAndTime}', 0)".format(transactionId = transactionId, senderCardNum = senderCardNum, receiverCardNum = receiverCardNum, currency = currency, sentAmount = sentAmount, dateAndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        connection.commit()
                        return 0
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception    

