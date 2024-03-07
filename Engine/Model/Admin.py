
class Admin:
    def __init__(self, email, password, firstName, lastName, address, city, country, phoneNum):
        self.email = email 
        self.password = password  
        self.firstName = firstName  
        self.lastName = lastName  
        self.address = address  
        self.city = city  
        self.country = country  
        self.phoneNum = phoneNum  
        
    def __repr__(self):
        return f"Admin(email={self.email}, password={self.password}, firstName={self.firstName}, lastName={self.lastName}, address={self.address}, city={self.city}, country={self.country}, phoneNum={self.phoneNum})"
