from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup
from .video import Video
from .subtitle import Subtitle

class Debate:
    def __init__(self, url) -> None:
        self.url = url
        self.__soup = self.__getSoup()
        self.title = self.__getTitle()
        self.subtitle = Subtitle(self.__soup, self.url)
        self.video = Video(self.__soup)
        self.date = self.__getDate()
        self.readable_date = self.__getReadableDate()


    def __getSoup(self) -> BeautifulSoup:
        if not re.match(r"^https?://", self.url):
            # Throw an error if the URL doesn't start with http or https
            raise ValueError("Invalid URL")

        # Request the URL
        r = requests.get(self.url)
        assert r.status_code == 200

        # Parse the HTML
        soup = BeautifulSoup(r.text, "html.parser")

        return soup

    def __getTitle(self) -> str:
        # Get the title of the video
        title = self.__soup.find("title").text

        # Remove the " | Debat Gemist" part of the title
        title = title.replace(" | Debat Gemist", "")

        return title
    
    def __getDate(self) -> datetime:
        # Find the time tag and get the datetime attribute
        date = self.__soup.find("time").get("datetime", None)

        # String to datetime
        date = datetime.strptime(date, "%Y-%m-%d")

        return date

    def __getReadableDate(self) -> str:
        # Find the time tag and get the inner text
        date = self.__soup.find("time").text

        return date