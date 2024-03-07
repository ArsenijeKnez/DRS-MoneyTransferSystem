
import requests
 
class CurrencyConverter:
    rates = {}  # empty dict to store the conversion rates
    
    def __init__(self):
        data = requests.get("http://data.fixer.io/api/latest?access_key=9570a750671ca394412d70f2ba1a05be").json()  # fetches the exchange rates from the API
        self.rates = data["rates"]  # extracting only the rates from the json data
 
    def convert(self, currencyFrom, currencyTo, amount):    # vrati konvertovanu vrijednost (amount je u currencyFrom valuti)
        currencyFrom = currencyFrom.upper()
        currencyTo = currencyTo.upper()

        if currencyFrom != currencyTo :
            if currencyFrom == "EUR":  # EUR --> RSD ili USD
                amount = self.__convertFromEuro(currencyTo, amount)
            elif currencyTo == "EUR":  # RSD ili USD --> EUR
                amount = self.__convertToEuro(currencyFrom, amount)
            else:  # ako je izmedju RSD i USD, konvertujem iz currencyFrom u EUR, pa iz EUR u currencyTo
                amount = self.__convertToEuro(currencyFrom, amount)
                amount = self.__convertFromEuro(currencyTo, amount)
                    
        return amount
    
    def __convertToEuro(self, currencyFrom, amount):
        amount /= self.rates[currencyFrom]
        return amount
        
    def __convertFromEuro(self, currencyTo, amount):
        amount *= self.rates[currencyTo]
        return amount
    
    def test(self):
        print("\n\n******** RSD --> EUR ********")
        print(2323)
        print(self.convert("RSD", "EUR", 2323))
        print("*****************************\n\n")
    
        print("******** EUR --> RSD ********")
        print(16)
        print(self.convert("EUR", "RSD", 16))
        print("*****************************\n\n")
    
        print("******** USD --> EUR ********")
        print(22)
        print(self.convert("USD", "EUR", 22))
        print("*****************************\n\n")
    
        print("******** EUR --> USD ********")
        print(16)
        print(self.convert("EUR", "USD", 16))
        print("*****************************\n\n")
        
        print("******** RSD --> USD ********")
        print(2323)
        print(self.convert("RSD", "USD", 2323))
        print("*****************************\n\n")

        print("******** USD --> RSD ********")
        print(22)
        print(self.convert("USD", "RSD", 22))
        print("*****************************\n\n")
        