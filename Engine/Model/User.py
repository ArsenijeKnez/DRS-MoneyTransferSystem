
class User:
    def __init__(self, email, password, firstName, lastName):
        self.email = email 
        self.password = password  
        self.firstName = firstName  
        self.lastName = lastName
        
    def __repr__(self):
        return f"User(email={self.email}, password={self.password}, firstName={self.firstName}, lastName={self.lastName})"
