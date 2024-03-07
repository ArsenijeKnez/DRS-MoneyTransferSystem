
class TransactionIdHelper:
    def readAndInsertFirstAvailable(self, cursor):
        transactionId = self.__readFirstAvailable(cursor)                        
        cursor.execute("insert into transaction_id values ({transactionId})".format(transactionId = transactionId))
                    
        return transactionId

    def delete(self, cursor, transactionId):
        cursor.execute("delete from transaction_id where value = {}".format(transactionId))
        

    def __readAll(self, cursor):
        cursor.execute("select value from transaction_id order by value asc")
        return cursor.fetchall()

    def __readFirstAvailable(self, cursor):
        tupleList = self.__readAll(cursor)
        
        unavailableIds = self.__readAll(cursor)  # unavailableIds je lista torki, a u svakoj torki je samo id, na nultoj poziciji
        id = 1
        while (True):
            if id > len(unavailableIds) or (id != unavailableIds[id - 1][0]):   
                break
                        
            # DEBUG: print(f"{id}, {unavailableIds[id - 1][0]}")
            id += 1
            
        return id 