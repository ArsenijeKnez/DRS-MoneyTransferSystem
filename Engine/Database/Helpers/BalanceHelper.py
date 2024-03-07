from Database.Helpers.CardHelper import CardHelper
from Utils.EmailSender import EmailSender

class BalanceHelper:
    def insert(self, cursor, cardNum, currency):
        cursor.execute("insert into balance values ('{cardNum}', '{currency}', 0)".format(cardNum = cardNum, currency = currency))
    
    def exists(self, cursor, cardNum, currency):
        cursor.execute("select count(*) from balance where card_num = '{cardNum}' and currency = '{currency}'".format(cardNum = cardNum, currency = currency))
                    
        if cursor.fetchone()[0] == 0:
            return False
        else:
            return True    

    def amountGreaterOrEqualThan(self, cursor, cardNum, currency, amount):
        cursor.execute("select amount from balance where card_num = '{cardNum}' and currency = '{currency}'".format(cardNum = cardNum, currency = currency))
        if cursor.fetchone()[0] >= amount:
            return True
        else:
            return False    

    def sendEmailTransactionNotExecuted(self, senderCardNum, receiverCardNum, currency, sentAmount, mail):
        cardHelper = CardHelper()
        emailSender = EmailSender()
        
        # Stavio sam ovo u try blok zato sto necu da mi ova metoda baci exception (necu da se desi return ReturnValues.exception zbog ove metode)
        try:
            senderEmail = cardHelper.readOwnerEmail(senderCardNum)
            if senderEmail is not None:  # moram da provjerim jer se moze desiti da je uklonio karticu sa naloga, pa onda u bazi owner_email postane null i readOwnerEmail() vrati None
                emailSender.sendEmailTransactionNotExecuted(senderEmail, senderCardNum, receiverCardNum, currency, sentAmount, mail)
        except Exception as e:
            print(e)

    def sendEmailsTransactionExecuted(self, senderCardNum, receiverCardNum, currency, sentAmount, mail):
        cardHelper = CardHelper()
        emailSender = EmailSender()
        
        # Stavio sam ovo u try blok zato sto necu da mi ova metoda baci exception (necu da se desi rollback zbog ove metode)
        # Uradio sam ovo ovako jer onda u slucaju da slanje mejla sender-u baci exception, slanje mejla receiver-u ce biti izvrseno
        try:
            senderEmail = cardHelper.readOwnerEmail(senderCardNum)
            if senderEmail is not None:  # moram da provjerim jer se moze desiti da je uklonio karticu sa naloga, pa onda u bazi owner_email postane null i readOwnerEmail() vrati None
                emailSender.sendEmailTransactionExecuted(senderEmail, senderCardNum, receiverCardNum, currency, sentAmount, mail)
        except Exception as e:
            print(e)            

            receiverEmail = cardHelper.readOwnerEmail(receiverCardNum)
            if receiverEmail is not None:  
                emailSender.sendEmailTransactionExecuted(receiverEmail, senderCardNum, receiverCardNum, currency, sentAmount, mail)
            
            return
        
        # Stavio sam ovo u try blok zato sto necu da mi ova metoda baci exception (necu da se desi rollback zbog ove metode)
        try:
            receiverEmail = cardHelper.readOwnerEmail(receiverCardNum)
            if receiverEmail is not None:  
                emailSender.sendEmailTransactionExecuted(receiverEmail, senderCardNum, receiverCardNum, currency, sentAmount, mail)
        except Exception as e:
            print(e)            
