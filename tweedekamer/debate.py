import requests
import re
from bs4 import BeautifulSoup
from enum import Enum

class DebateType(Enum):
    ANY = ""
    PLENARY = "field_debate_type%3A1"
    COMMITTEE = "field_debate_type%3A154189"

class Debate:
    def __init__(self, url):
        self.url = url
        self.soup = self.__getSoup()
        self.title = self.getTitle()

    def __getSoup(self):
        if not re.match(r"^https?://", self.url):
            # Throw an error if the URL doesn't start with http or https
            raise ValueError("Invalid URL")

        # Request the URL
        r = requests.get(self.url)
        if r.status_code != 200:
            print("Error requesting URL")
            exit(1)

        # Parse the HTML
        soup = BeautifulSoup(r.text, "html.parser")

        return soup

    def getTitle(self):
        # Get the title of the video
        title = self.soup.find("title").text

        # Remove the " | Debat Gemist" part of the title
        title = title.replace(" | Debat Gemist", "")

        # make title folder name safe
        title = title.replace(" ", "_")
        title = title.replace(":", "_")
        title = title.replace("?", "_")
        title = title.replace("/", "_")
        title = title.replace("\\", "_")
        title = title.replace("*", "_")
        title = title.replace("|", "_")
        title = title.replace("(", "_")
        title = title.replace(")", "_")

        title = title.strip()

        return title

    def getVideoLink(self):
        # Find the download link in the HTML
        # The .mp4 link is found in an input where the id starts with "edit-debate-file-options-download-"
        # Then the link is found in the value attribute of that input
        
        download_link = self.soup.find(
            "input", {"id": re.compile(r"^edit-debate-file-options-download-")}
        )

        if download_link is None:
            # Find an input id that starts with "edit-debate-file-options-azure-httpsdebatgemist"
            download_link = self.soup.find(
                "input", {"id": re.compile(r"^edit-debate-file-options-azure-httpsdebatgemist")}
            )
            download_link = download_link["value"]
            download_link = download_link.replace("azure_", "")
        else:
            # Remove the "download_" prefix from the link
            download_link = download_link.replace("download_", "")

        return download_link

    def getSubtitleFilename(self):
        # Find the subtitle link in the HTML
        # Find the input tag where the id starts with "edit-debate-file-options-" and the value ends with ".srt"
        subtitle_link = self.soup.find(
            "input",
            {
                "id": re.compile(r"^edit-debate-file-options-"),
                "value": re.compile(r".srt$"),
            },
        )["value"]

        return subtitle_link

    def getSubtitleText(self):
        subtitle = self.getSubtitle()

        # Remove the index number from the subtitle
        subtitle = re.sub(r"^\d+\s", "", subtitle, flags=re.MULTILINE)

        # Remove the timecode from the subtitle
        subtitle = re.sub(r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s", "", subtitle, flags=re.MULTILINE)

        # Remove the empty lines
        subtitle = re.sub(r"^\s*$", "", subtitle, flags=re.MULTILINE)

        return subtitle

    def getSubtitle(self, path = ""):
        subtitle_link = self.getSubtitleFilename()

        # Get the form-build-id from the HTML
        form_build_id = self.soup.find("input", {"name": "form_build_id"})["value"]

        # Create a POST request with the following form-data
        # form_build_id: form_build_id
        # form_id: "debatgemist_download_video_form"
        # op: "Download"
        # debate_file_options: subtitle_link
        data = {
            "form_build_id": form_build_id,
            "form_id": "debatgemist_download_video_form",
            "op": "Download",
            "debate_file_options": subtitle_link,
        }

        # Request the subtitle file
        r = requests.post(self.url, data=data)

        if r.status_code != 200:
            print("Error requesting URL")
            exit(1)

        # Return the subtitle file as string
        return r.text


