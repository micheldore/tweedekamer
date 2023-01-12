from nltk.tokenize import RegexpTokenizer

class Speach:
    def __init__(self, debate, speaker):
        self.text = ""
        self.subtitle = ""
        self.tokenized = []

        try:
            self.text = debate.subtitle.getTextFromXtoY(speaker.start_time, speaker.end_time)
            self.subtitle = debate.subtitle.getFromXtoY(speaker.start_time, speaker.end_time)
            self.tokenized = self.__tokenize()
        except:
            pass


    def __tokenize(self):
        tokenizer = RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(self.text.lower())

        return tokens