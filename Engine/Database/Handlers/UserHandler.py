from mysql.connector import connect
from Database.Helpers.UserHelper import UserHelper
from Enums.ReturnValues import ReturnValues
from Model.User import User
from Utils.EmailSender import EmailSender

class UserHandler:
    userHelper = UserHelper()

    # Ako u bazi postoji user sa prosledjenim email-om, onda se vrati User objekat sa podacima tog user-a, a ako ne postoji onda se vrati ReturnValues.doesntExist
    def read(self, email):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    cursor.execute("select * from user where email = '{email}'".format(email = email))
                    
                    userTuple = cursor.fetchone()
                        
                    if userTuple is None:
                        return ReturnValues.doesntExist
                    else:
                        return self.userHelper.getObjectFromTuple(userTuple)
        except Exception as e:
            print(e)
            return ReturnValues.exception
    
    # Doda novog user-a u bazu. Ako u bazi vec postoji user sa prosledjenim email-om, onda vrati ReturnValues.alreadyExists.
    def insert(self, user, mail):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    if self.userHelper.exists(cursor, user.email):
                        return ReturnValues.alreadyExists
        
                    try:
                        cursor.execute("insert into user values ('{email}', '{password}', '{firstName}', '{lastName}')".format(email = user.email, password = user.password, firstName = user.firstName, lastName = user.lastName))
                        
                        emailSender = EmailSender()
                        emailSender.sendEmailCredentials(user.email, user.password, mail)
                        
                        connection.commit()  # commit se nalazi posle slanja mejla jer ako se desi exception pri slanju mejla, onda user nece dobiti kredencijale pa ne treba ni da se ubacuje u bazu
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception
    
    # Izmjeni user-a u bazi ciji email je "oldEmail". Ako u bazi vec postoji user ciji email je isti kao user.email, onda vrati ReturnValues.alreadyExists
    def update(self, oldEmail, user):  
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    if user.email != oldEmail and self.userHelper.exists(cursor, user.email):
                        return ReturnValues.alreadyExists                    

                    try:
                        cursor.execute("update user set email = '{newEmail}', password = '{password}', first_name = '{firstName}', last_name = '{lastName}' where email = '{oldEmail}'".format(newEmail = user.email, password = user.password, firstName = user.firstName, lastName = user.lastName, oldEmail = oldEmail))
                        # Ne treba da apdejtujem owner_email u card tabeli jer se to uradi automatski (on update cascade)                        

                        connection.commit()
                    except Exception as e:
                        print(e)
                        connection.rollback()
                        return ReturnValues.exception
        except Exception as e:
            print(e)
            return ReturnValues.exception
        
