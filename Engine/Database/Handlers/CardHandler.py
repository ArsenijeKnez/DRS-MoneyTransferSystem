from ast import Try
from mysql.connector import connect
from Enums.ReturnValues import ReturnValues
from Database.Helpers.CardHelper import CardHelper

class CardHandler:
    cardHelper = CardHelper()    

    # Postavi owner_email na "email za card u bazi ciji number je "cardNum". Vrati ReturnValues.doesntExist ako u bazi ne postoji card ciji number je "cardNum", a vrati ReturnValues.alreadyExists ako u bazi vec postoi neki user koji je povezan sa karticom ciji number je "cardNum". Poziva se kada korisnik unese novu karticu.
    def setOwnerEmail(self, cardNum, email):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    if not self.cardHelper.exists(cursor, cardNum):
                        return ReturnValues.doesntExist
                    
                    if self.cardHelper.hasOwner(cursor, cardNum):
                        return ReturnValues.alreadyExists

                    try:    
                        cursor.execute("update card set owner_email = '{email}' where number = '{cardNum}'".format(email = email, cardNum = cardNum))
                        connection.commit()
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception

    # Postavi verified na 1 za card u bazi ciji number je "cardNum". Poziva se kada admin prihvati povezivanje kartice za nalog.
    def verify(self, cardNum):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("update card set verified = 1 where number = '{cardNum}'".format(cardNum = cardNum))
                        connection.commit()
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception

    # Postavi owner_email na null za karticu ciji number je "cardNum". Poziva se kada admin odbije povezivanje kartice za nalog.
    def setOwnerEmailToNull(self, cardNum):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    try:    
                        cursor.execute("update card set owner_email = null where number = '{cardNum}'".format(cardNum = cardNum))
                        connection.commit()
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception

    # Postavi owner_email na null i verified na 0 za karticu ciji number je "cardNum". Poziva se kada korisnik ukloni karticu sa svog naloga.
    def setOwnerEmailToNullAndVerifiedTo0(self, cardNum):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    try:    
                        cursor.execute("update card set owner_email = null, verified = 0 where number = '{cardNum}'".format(cardNum = cardNum))
                        connection.commit()
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception

