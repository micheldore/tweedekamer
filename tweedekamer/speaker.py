import math


class Speaker:
    def __init__(self, data):
        self.data = data
        self.name = self.__getName()
        self.short_name = self.__getShortName()
        self.party = self.__getParty()
        self.function = self.__getFunction()
        self.start_time = self.__getStartTime()
        self.end_time = self.__getEndTime()
        self.image_url = self.__getImageUrl()
        self.duration = math.abs(self.end_time - self.start_time)
    
    def __getName(self):
        return self.data.get("name", "")
    
    def __getShortName(self):
        return self.data.get("name_short", "")

    def __getParty(self):
        full_function = self.data.get("parliamentary_party", "")
        
        try:
            party = full_function.split(" - ")[0]
        except:
            raise IndexError("Could not find party in full function description")

        return party

    def __getFunction(self):
        full_function = self.data.get("parliamentary_party", "")

        try:
            function = full_function.split(" - ")[1]
        except:
            raise IndexError("Could not find function in full function description")

        return function
    
    def __getStartTime(self):
        start = self.data.get("start", 0)
        start = max(start, 0)
        start = int(start)

        return start
    
    def __getEndTime(self):
        end = self.data.get("end", 0)
        end = max(end, 0)
        end = int(end)

        return end

    def __getImageUrl(self):
        return self.data.get("speaker_image", "")


