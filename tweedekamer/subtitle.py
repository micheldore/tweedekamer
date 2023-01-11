import re
import requests

class Subtitle:
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.raw = self.get()
        self.text = self.__getText()

    def getFilename(self):
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

    def __getText(self):
        clean_text = self.raw

        # Remove the index number from the subtitle
        clean_text = re.sub(r"^\d+\s", "", clean_text, flags=re.MULTILINE)

        # Remove the timecode from the subtitle
        clean_text = re.sub(r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s", "", clean_text, flags=re.MULTILINE)

        # Remove the empty lines
        clean_text = re.sub(r"^\s*$", "", clean_text, flags=re.MULTILINE)

        return clean_text

    def get(self):
        subtitle_link = self.getFilename()

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