from mysql.connector import connect
from mysql.connector.errors import Error
from locale import currency
from datetime import datetime
from Database.Helpers.BalanceHelper import BalanceHelper
from Database.Helpers.BankCheckHelper import BankCheckHelper
from Database.Helpers.TransactionHelper import TransactionHelper
from Database.Helpers.CardHelper import CardHelper
from Enums.ReturnValues import ReturnValues
from Model.Balance import Balance
from Model.BankCheck import BankCheck
from Utils.CurrencyConverter import CurrencyConverter
from Model.Transaction import Transaction
from Utils.EmailSender import EmailSender

class BalanceHandler:
    balanceHelper = BalanceHelper()    

    # Uveca balance amount kartice ciji number je "cardNum" za amount bank check-a iz baze ciji code je "checkCode". Ako kartica nije verifikovana, vrati return ReturnValues.cardNotVerified. Ako u bazi ne postoji bank check ciji code je "checkCode", onda vrati ReturnValues.doesntExist.
    def depositWithCheck(self, checkCode, cardNum):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    bankCheckHelper = BankCheckHelper()
                    cardHelper = CardHelper()
                    
                    if not cardHelper.verified(cursor, cardNum):
                        return ReturnValues.cardNotVerified                        

                    try:
                        bankCheck = bankCheckHelper.readAndDelete(cursor, checkCode)
                        if bankCheck == ReturnValues.doesntExist:
                            return ReturnValues.doesntExist                        

                        if not self.balanceHelper.exists(cursor, cardNum, bankCheck.currency):
                            self.balanceHelper.insert(cursor, cardNum, bankCheck.currency)

                        cursor.execute("update balance set amount = amount + {bankCheckAmount} where card_num = '{cardNum}' and currency = '{currency}'".format(bankCheckAmount = bankCheck.amount, cardNum = cardNum, currency = bankCheck.currency))
                        connection.commit() 
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception
    
    # Konvertuje "amount" ("amount" je u currencyFrom valuti) novca iz "currencyFrom" u "currencyTo" valutu na kartici ciji number je "cardNum". Ako na toj kartici nema dovoljno novca u "currencyFrom" valuti onda vrati ReturnValues.insufficientFunds, a ako ta kartica nije verifikovana, onda vrati ReturnValues.cardNotVerified.
    def convert(self, cardNum, currencyFrom, currencyTo, amount): 
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    cardHelper = CardHelper()
                    if not cardHelper.verified(cursor, cardNum):
                        return ReturnValues.cardNotVerified
                    
                    converter = CurrencyConverter()    
                    convertedAmount = converter.convert(currencyFrom, currencyTo, amount)

                    if not self.balanceHelper.amountGreaterOrEqualThan(cursor, cardNum, currencyFrom, amount):
                        return ReturnValues.insufficientFunds                    

                    try:
                        if not self.balanceHelper.exists(cursor, cardNum, currencyTo):
                            self.balanceHelper.insert(cursor, cardNum, currencyTo)                   

                        cursor.execute("update balance set amount = amount - {amount} where card_num = '{cardNum}' and currency = '{currencyFrom}'".format(amount = amount, cardNum = cardNum, currencyFrom = currencyFrom))
                        cursor.execute("update balance set amount = amount + {convertedAmount} where card_num = '{cardNum}' and currency = '{currencyTo}'".format(convertedAmount = convertedAmount, cardNum = cardNum, currencyTo = currencyTo))
                        connection.commit()
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception

    # Poziva se u executeUnexecutedTransactions()
    def executeTransaction(self, senderCardNum, receiverCardNum, currency, sentAmount, mail):
        try:
            transactionHelper = TransactionHelper()
            
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    if not self.balanceHelper.amountGreaterOrEqualThan(cursor, senderCardNum, currency, sentAmount):
                        transactionHelper.deleteUnexecuted(cursor, senderCardNum, receiverCardNum)
                        connection.commit()

                        self.balanceHelper.sendEmailTransactionNotExecuted(senderCardNum, receiverCardNum, currency, sentAmount, mail)
                        return   
                    
                    try:
                        if not self.balanceHelper.exists(cursor, receiverCardNum, currency):
                            self.balanceHelper.insert(cursor, receiverCardNum, currency) 
                            
                        cursor.execute("update balance set amount = amount - {sentAmount} where card_num = '{senderCardNum}' and currency = '{currency}'".format(sentAmount = sentAmount, senderCardNum = senderCardNum, currency = currency))
                        cursor.execute("update balance set amount = amount + {sentAmount} where card_num = '{receiverCardNum}' and currency = '{currency}'".format(sentAmount = sentAmount, receiverCardNum = receiverCardNum, currency = currency))
                        
                        transactionHelper.setExecutedTo1(cursor, senderCardNum, receiverCardNum)
                        
                        connection.commit() 
                        
                        self.balanceHelper.sendEmailsTransactionExecuted(senderCardNum, receiverCardNum, currency, sentAmount, mail)
                    except Exception as e:
                        connection.rollback()
                        
                        print(e)
                        self.balanceHelper.sendEmailTransactionNotExecuted(senderCardNum, receiverCardNum, currency, sentAmount, mail)
        except Exception as e:
            print(e)
            self.balanceHelper.sendEmailTransactionNotExecuted(senderCardNum, receiverCardNum, currency, sentAmount, mail)
        
