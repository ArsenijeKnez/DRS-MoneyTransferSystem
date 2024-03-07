from Model.User import User

class UserHelper:
    def getObjectFromTuple(self, userTuple):
        return User(userTuple[0], userTuple[1], userTuple[2], userTuple[3])

    def getObjectListFromTupleList(self, userTupleList):
        users = []
        for userTuple in userTupleList:
            users.append(self.getObjectFromTuple(userTuple))

        return users
    
    def exists(self, cursor, email):
        cursor.execute("select count(*) from user where email = '{}'".format(email))
                    
        if cursor.fetchone()[0] == 0:
            return False
        else:
            return True 