import re
import requests
from nltk.tokenize import RegexpTokenizer

class Subtitle:
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.raw = self.get()
        self.text = self.__getText()
        self.tokenized = self.__tokenize()

    def getFilename(self):
        # Find the subtitle link in the HTML
        # Find the input tag where the id starts with "edit-debate-file-options-" and the value ends with ".srt"
        subtitle_link = self.soup.find(
            "input",
            {
                "id": re.compile(r"^edit-debate-file-options-"),
                "value": re.compile(r".srt$"),
            },
        )

        try:
            subtitle_link = subtitle_link["value"]
        except:
            subtitle_link = ""

        return subtitle_link

    def __getText(self):
        clean_text = self.cleanSubtitle(self.raw)

        return clean_text

    def cleanSubtitle(self, raw_subtitle):
        clean_text = raw_subtitle

        # Remove the index number from the subtitle
        clean_text = re.sub(r"^\d+\s", "", clean_text, flags=re.MULTILINE)

        # Remove the timecode from the subtitle
        clean_text = re.sub(r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s", "", clean_text, flags=re.MULTILINE)

        # Remove the empty lines
        clean_text = re.sub(r"^\s*$", "", clean_text, flags=re.MULTILINE)

        return clean_text

    def __tokenize(self):
        tokenizer = RegexpTokenizer(r"\w+")
        tokens = tokenizer.tokenize(self.text.lower())

        return tokens

    
    def getTextFromXtoY(self, x, y):
        raw = self.getFromXtoY(x, y)
        clean_text = self.cleanSubtitle(raw)

        return clean_text

    # Get subtitles from second x to second y
    def getFromXtoY(self, x, y):
        # Get the raw text
        raw_text = self.raw

        # Split the text into a list of lines
        lines = raw_text.splitlines()

        # Create a list to store the lines that are between x and y
        lines_in_range = []

        # Loop through the lines
        for line in lines:
            # Check if the line is a timecode
            # Example: 02:38:30,330 --> 02:38:35,620
            if re.match(r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d$", line):
                # Split the timecode into two parts
                timecode = line.split(" --> ")

                # Get the start and end time
                start_time = timecode[0]
                end_time = timecode[1]

                # Convert the start and end time to seconds
                start_time = self.__timecodeToSeconds(start_time)
                end_time = self.__timecodeToSeconds(end_time)

                # Check if the start and end time are between x and y
                if start_time >= x and end_time <= y:
                    # Add the timecode to the list
                    lines_in_range.append(line)
                else:
                    # Check if the start time is between x and y
                    if start_time >= x and start_time <= y:
                        # Add the timecode to the list
                        lines_in_range.append(line)

                    # Check if the end time is between x and y
                    if end_time >= x and end_time <= y:
                        # Add the timecode to the list
                        lines_in_range.append(line)
                if start_time > y:
                    break
            else:
                # Check if the line is between x and y
                if len(lines_in_range) > 0:
                    # Add the line to the list
                    lines_in_range.append(line)

        # Join the lines into a string
        text = "\n".join(lines_in_range)

        return text

    
    def __timecodeToSeconds(self, timecode):
        # Split the timecode into hours, minutes, seconds and milliseconds
        timecode = timecode.split(":")
        hours = int(timecode[0])
        minutes = int(timecode[1])
        seconds = int(timecode[2].split(",")[0])
        milliseconds = int(timecode[2].split(",")[1])

        # Convert the timecode to seconds
        seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000

        return seconds

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