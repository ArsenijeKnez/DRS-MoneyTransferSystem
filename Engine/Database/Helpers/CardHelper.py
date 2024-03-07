from Enums.ReturnValues import ReturnValues
from mysql.connector import connect
from mysql.connector.errors import Error

class CardHelper:
    def readOwnerEmail(self, cardNum):
        with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
            with connection.cursor() as cursor:
                cursor.execute("select owner_email from card where number = '{cardNum}'".format(cardNum = cardNum))
                return cursor.fetchone()[0]

    def exists(self, cursor, cardNum):
        cursor.execute("select count(*) from card where number = '{cardNum}'".format(cardNum = cardNum))
                    
        if cursor.fetchone()[0] == 0:
            return False
        else:
            return True

    def hasOwner(self, cursor, cardNum):
        cursor.execute("select owner_email from card where number = '{cardNum}'".format(cardNum = cardNum))
                    
        if cursor.fetchone()[0] is None:
            return False
        else:
            return True
        
    def verified(self, cursor, cardNum):
        cursor.execute("select verified from card where number = '{cardNum}'".format(cardNum = cardNum))
                    
        if cursor.fetchone()[0] == 0:
            return False
        else:
            return True