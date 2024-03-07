from datetime import datetime

class DateAndTimeParser:
    def parse(dateAndTimeString): # dateAndTimeString je u formatu YYYY-MM-DD hh:mm:ss
        year = int(dateAndTimeString[0:3])
        month = int(dateAndTimeString[5:6].lstrip("0"))
        day = int(dateAndTimeString[8:9].lstrip("0"))  
        
        hour = int(dateAndTimeString[11:12].lstrip("0"))
        minute = int(dateAndTimeString[14:15].lstrip("0"))
        second = int(dateAndTimeString[17:18].lstrip("0"))
        
        return datetime(year, month, day, hour, minute, second)
        