from Model.Admin import Admin

class AdminHelper:
     def getObjectFromTuple(self, adminTuple):
        return Admin(adminTuple[0], adminTuple[1], adminTuple[2], adminTuple[3], adminTuple[4], adminTuple[5], adminTuple[6], adminTuple[7])
