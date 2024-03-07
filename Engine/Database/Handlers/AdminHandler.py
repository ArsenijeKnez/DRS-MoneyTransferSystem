from mysql.connector import connect
from Database.Helpers.AdminHelper import AdminHelper
from Enums.ReturnValues import ReturnValues

class AdminHandler:
    adminHelper = AdminHelper()    

    # Ako u bazi postoji admin sa prosledjenim email-om, onda se vrati Admin objekat sa podacima tog admin-a, a ako ne postoji onda se vrati ReturnValues.doesntExist
    def read(self, email):
        try:
            with connect(host="localhost", user="root", password="programiranje", database="drs") as connection:
                with connection.cursor() as cursor:
                    cursor.execute("select * from admin where email = '{email}'".format(email = email))
                    
                    adminTuple = cursor.fetchone()
                    if adminTuple is None:
                        return ReturnValues.doesntExist
                    else:
                        return self.adminHelper.getObjectFromTuple(adminTuple)
        except Exception as e:
            print(e)
            return ReturnValues.exception
