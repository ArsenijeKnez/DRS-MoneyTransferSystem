from mysql.connector import connect
from DTOs.CardAndBalanceOfUserDTO import CardAndBalanceOfUserDTO
from DTOs.CardWithOwnerDataDTO import CardWithOwnerDataDTO
from DTOs.TransactionWithUserDataDTO import TransactionWithUserDataDTO
from Database.Handlers.BalanceHandler import BalanceHandler
from Database.Helpers.TransactionHelper import TransactionHelper
from Enums.ReturnValues import ReturnValues
from Model.User import User
from Model.Transaction import Transaction
from Database.Handlers.TransactionHandler import TransactionHandler
from Database.Handlers.UserHandler import UserHandler
from Database.Helpers.ComplexHelper import ComplexHelper

class ComplexHandler:  
    complexHelper = ComplexHelper()    

    # Vrati listu CardAndBalanceOfUserDTO objekata u kojoj su podaci o karticama i balansima korisnika ciji email je "email"
    def readCardsAndBalancesOfUser(self, email):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    cursor.execute("select number, exp_date, cvc, verified, currency, amount from user inner join card on user.email = card.owner_email inner join balance on card.number = balance.card_num where email = '{}'".format(email))
                    
                    cardAndBalanceOfUserDTO = CardAndBalanceOfUserDTO()
                    return cardAndBalanceOfUserDTO.getObjectListFromTupleList(cursor.fetchall())
        except Exception as e:
            print(e)
            return ReturnValues.exception
    
    # Vrati listu TransactionWithUserDataDTO objekata u kojoj su podaci o poslednjih "numberOfTransactions" transakcija zajedno sa podacima o sender-u i receiver-u. Ako je sender ili receiver uklonio karticu sa naloga nakon trazenja da se izvrsi transakcija, onda ce u objektima u listi koja se vraca da bude None za polja koja se odnose na vlasnika kartice
    def readLastTransactionsWithUserData(self, numberOfTransactions):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    transactionHelper = TransactionHelper()       
                    lastTransactions = transactionHelper.readLastExecuted(cursor, numberOfTransactions)
                    cardsWithUserData = self.complexHelper.readAllCardsWithUserData(cursor)

                    resultList = []
                    # u resultList stavi elemente kod kojih su transaction i sender popunjeni, a receiver je None
                    for transaction in lastTransactions:
                        for cardWithUserData in cardsWithUserData:
                            if transaction.senderCardNum == cardWithUserData[4]:
                                resultList.append(TransactionWithUserDataDTO(transaction, User(cardWithUserData[0], cardWithUserData[1], cardWithUserData[2], cardWithUserData[3]), None))
                    
                    # u elementima resultList-a popuni receiver polja
                    for element in resultList:
                        for cardWithUserData in cardsWithUserData:
                            if element.transaction.receiverCardNum == cardWithUserData[4]:
                                element.receiver = User(cardWithUserData[0], cardWithUserData[1], cardWithUserData[2], cardWithUserData[3])
                    
                    return resultList
        except Exception as e:
            print(e)
            return ReturnValues.exception
    
    # Vrati listu CardWithOwnerDataDTO objekata u kojoj su podaci o neverifikovanim karticama i njihovim vlasnicima.
    def readUnverifiedCardsWithOwnerData(self):  
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    cursor.execute("select email, first_name, last_name, number, exp_date, cvc from user inner join card on user.email = card.owner_email where verified = 0")
                    
                    cardWithOwnerData = CardWithOwnerDataDTO()
                    return cardWithOwnerData.getObjectListFromTupleList(cursor.fetchall())
        except Exception as e:
            print(e)
            return ReturnValues.exception

    # Izvrsi transakcije koje su na cekanju
    def executeUnexecutedTransactions(self, mail):
        transactionHelper = TransactionHelper()    
        balanceHandler = BalanceHandler()

        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    unexecutedTransactions = transactionHelper.readUnexecutedTransactions(cursor)
        except Exception as e:
            print(e)
            return ReturnValues.exception

        transactionsWithUserData = self.complexHelper.readTransactionsWithUserData(unexecutedTransactions)

        for transaction in unexecutedTransactions:
            balanceHandler.executeTransaction(transaction.senderCardNum, transaction.receiverCardNum, transaction.currency, transaction.sentAmount, mail)
      
        return transactionsWithUserData;
    
