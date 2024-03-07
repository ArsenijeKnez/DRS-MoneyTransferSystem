from mysql.connector import connect
from DTOs.TransactionWithUserDataDTO import TransactionWithUserDataDTO
from Enums.ReturnValues import ReturnValues
from Model.User import User

class ComplexHelper:
    def readTransactionsWithUserData(self, transactions):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    cardsWithUserData = self.readAllCardsWithUserData(cursor)
                    
                    resultList = []
                    # u resultList stavi elemente kod kojih su transaction i sender popunjeni, a receiver je None
                    for transaction in transactions:
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
    
    def readAllCardsWithUserData(self, cursor):
        cursor.execute("select * from user right outer join card on user.email = card.owner_email")
        return cursor.fetchall()