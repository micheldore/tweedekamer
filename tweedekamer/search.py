import re
import requests
import csv
from bs4 import BeautifulSoup
from .debate import Debate
from .enums.debate_type import DebateType
from .enums.sort_direction import SortDirection
from .enums.sort_type import SortType


class Search:
    def __init__(self, query, start_date: str = "", end_date: str = "", debate_type = DebateType.ANY, sort = SortType.RELEVANCE, sort_direction = SortDirection.DESC, limit = 10) -> None:
        self.base_url = "https://debatgemist.tweedekamer.nl"
        self.result = self.__getDebates(query, start_date, end_date, debate_type, sort, sort_direction, limit)

    def __checkAndGenerateSearchUrl(self, query, start_date, end_date, debate_type, sort = SortType.RELEVANCE, sort_direction = SortDirection.DESC, limit = 10) -> str:
        base_url = "https://debatgemist.tweedekamer.nl"

        search_url = base_url + "/zoeken?search_api_views_fulltext={}"
        search_url = search_url.format(query)

        dates_added = False

        if start_date and end_date:
            # Check date format
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", start_date):
                raise ValueError("Invalid start date, format should be YYYY-MM-DD")

            if not re.match(r"^\d{4}-\d{2}-\d{2}$", end_date):
                raise ValueError("Invalid end date, format should be YYYY-MM-DD")

            search_url = search_url + "&f[0]=created:[{}T00:00:00Z TO {}T00:00:00Z]"
            search_url = search_url.format(start_date, end_date)

            dates_added = True
        
        if debate_type != DebateType.ANY:
            if dates_added:
                search_url = search_url + "&f[1]={}"
            else:
                search_url = search_url + "&f[0]={}"

            search_url = search_url.format(debate_type.value)

        search_url = search_url + "&sort={}&order"
        search_url = search_url.format(sort.value, sort_direction.value)

        assert limit > 0
        assert search_url != base_url

        return search_url

    def __getSoup(self, search_url) -> BeautifulSoup:
        r = requests.get(search_url)
        assert r.status_code == 200

        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    # Based on a text query returns a list of debate urls
    def __getDebates(self, query, start_date = "", end_date = "", debate_type = DebateType.ANY, sort = SortType.RELEVANCE, sort_direction = SortDirection.DESC, limit = 10):
        self.__checkAndGenerateSearchUrl(query, start_date, end_date, debate_type, sort, sort_direction, limit)
        debate_urls = self.__getDebateUrls(query, start_date, end_date, debate_type, sort, sort_direction, limit)
        if debate_urls:
            return [Debate(url) for url in debate_urls]
        else:
            return []
        
    
    def to_csv(self, filename, separate_speakers = True, delimiter = ","):
        if delimiter not in [";", ","]:
            raise ValueError("Invalid delimiter, only ';' and ',' are supported")

        with open('{}.csv'.format(filename), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=delimiter, quoting=csv.QUOTE_ALL)

            if separate_speakers:
                writer.writerow(["title", "date", "url", "video_url", "speaker", "party", "tokenized", "subtitle"])
            else:
                writer.writerow(["title", "date", "url", "video_url", "tokenized", "subtitle", "text"])

            for debate in self.result:
                if not separate_speakers:
                    writer.writerow([debate.title, debate.date, debate.url, debate.video.url, debate.subtitle.tokenized, debate.subtitle.raw, debate.subtitle.text])
                    continue

                for speaker in debate.speakers:
                    writer.writerow([debate.title, debate.date, debate.url, debate.video.url, speaker.name, speaker.party, speaker.speach.tokenized, speaker.speach.subtitle])
            
            file.close()
                        


    def __getDebateUrls(self, query, start_date = None, end_date = None, debate_type = DebateType.ANY, sort = SortType.RELEVANCE, sort_direction = SortDirection.DESC, limit = 10):
        done = False
        search_url = self.__checkAndGenerateSearchUrl(query, start_date, end_date, debate_type, sort, sort_direction, limit)
        debates = []

        while not done:
            soup = self.__getSoup(search_url)

            # Find all a href tags where the class is "video-thumb"
            temp_debates = soup.find_all("a", {"class": "video-thumb"})
            temp_debates = [self.base_url + debate["href"] for debate in temp_debates]

            for debate in temp_debates:
                if len(debates) >= limit:
                    done = True
                    break

                debates.append(debate)

            # Find the next page link, an a tag with the title "Ga naar volgende pagina"
            next_page = soup.find("a", {"title": "Ga naar volgende pagina"})

            if next_page:
                search_url = self.base_url + next_page["href"]
            else:
                done = True

        return debates