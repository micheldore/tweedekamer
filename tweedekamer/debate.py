from datetime import datetime
import json
import requests
import re
from bs4 import BeautifulSoup
from .video import Video
from .subtitle import Subtitle
from .speaker import Speaker

class Debate:
    def __init__(self, url) -> None:
        self.url = url
        self.__soup = self.__getSoup()
        self.title = self.__getTitle()
        self.subtitle = Subtitle(self.__soup, self.url)
        self.video = Video(self.__soup)
        self.date = self.__getDate()
        self.readable_date = self.__getReadableDate()
        self.speakers = self.__getSpeakers()

    def __getSpeakersFromJSON(self):
        # Find the video tag with id "ys-videojs" and get the data-setup attribute
        # The data-setup attribute contains a JSON string with the speakers
        speakers_json = self.__soup.find("video", {"id": "ys-videojs"})

        if speakers_json is None:
            return []
        
        speakers_json = speakers_json["data-setup"]

        # Convert the JSON string to a Python dictionary
        speakers = json.loads(speakers_json)
        return speakers.get("plugins").get("chapterdock").get("chapters", [])

    def __getSpeakers(self):
        speakers = [Speaker(self, data) for data in self.__getSpeakersFromJSON()]
        return speakers


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
        title = ""

        try:
            # Get the title of the video
            title = self.__soup.find("title").text

            # Remove the " | Debat Gemist" part of the title
            title = title.replace(" | Debat Gemist", "")
        except:
            pass

        return title
    
    def __getDate(self) -> datetime:
        date = None

        try:
            # Find the time tag and get the datetime attribute
            date = self.__soup.find("time").get("datetime", None)

            # String to datetime
            date = datetime.strptime(date, "%Y-%m-%d")
        except:
            pass

        return date

    def __getReadableDate(self) -> str:
        date = ""

        try:
            # Find the time tag and get the inner text
            date = self.__soup.find("time").text
        except:
            pass

        return date