from flask_mail import Message,Mail


class EmailSender:
    # Posalje korisniku email koji sadrzi email i password korisnika.
    def sendEmailCredentials(self, email, password, mail):
        subject = 'Your bank account credentials'
        recipients = [email]
        body = f"Welcome to Drs Team 2 System for transferring money, here are your credentials.\n Email: {email}, Password: {password}"

        message = Message(subject=subject, recipients=recipients, body=body)
    
        try:
            mail.send(message)
            return 'Email sent successfully!'
        except Exception as e:
            return str(e)

    # Posalje email da je transakcija uspjesno izvrsena. Kao parametar "email" se prosledjuje i email sender-a i email receiver-a, tj. ova ista metoda se poziva i za slanje sender-u i za slanje receiver-u, pa obojici stigne isti email.
    def sendEmailTransactionExecuted(self, email, senderCardNum, receiverCardNum, currency, sentAmount, mail):
        subject = 'Transaction executed'
        recipients = [email]
        body = f"Money transaction completed.\n Sender card: {senderCardNum}, receiver card: {receiverCardNum}, currency {currency}, amount {sentAmount}"

        message = Message(subject=subject, recipients=recipients, body=body)
    
        try:
            mail.send(message)
            return 'Email sent successfully!'
        except Exception as e:
            return str(e)
        
    # Posalje email sender-u da izvrsavanje transakcije nije uspjelo
    def sendEmailTransactionNotExecuted(self, senderEmail, senderCardNum, receiverCardNum, currency, sentAmount, mail):
        subject = 'Transaction not executed'
        recipients = [senderEmail]
        body = f"We regret to inform you that the folowing transaction could not be executed.\n Sender card: {senderCardNum}, receiver card: {receiverCardNum}, currency {currency}, amount {sentAmount}"

        message = Message(subject=subject, recipients=recipients, body=body)
    
        try:
            mail.send(message)
            return 'Email sent successfully!'
        except Exception as e:
            return str(e)