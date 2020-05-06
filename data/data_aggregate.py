

class Data_Rabbit():
    # Parses csv into dataframe
    def parse(self, fstream):
        return ""

    # Download file from google drive (csv)
    def fetch(self, url):
        return self.parse(open("", "rd"))

    def __init__(self):
        FILES = {
            "John Hopkins Raw US": ("jh_us", "test"),
            "BNO US": ("bno_us", "test")
        }
        data = {}
        MORNING_CHECK = False
        EVENING_CHECK = False
        for x in FILES.keys():
            data[x] = self.fetch(FILES[x][1])
