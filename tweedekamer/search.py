import re
import requests
from bs4 import BeautifulSoup
from debate import Debate, DebateType

class Search:
    def __init__(self) -> None:
        self.base_url = "https://debatgemist.tweedekamer.nl"

    def __checkAndGenerateSearchUrl(self, query: str, start_date: str, end_date: str, debate_type: DebateType) -> str:
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

        assert search_url != base_url

        return search_url

    def __getSoup(self, search_url: str) -> BeautifulSoup:
        r = requests.get(search_url)
        assert r.status_code == 200

        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    # Based on a text query returns a list of debate urls
    def getDebates(self, query: str, start_date: str = "", end_date: str = "", debate_type: DebateType = DebateType.ANY):
        self.__checkAndGenerateSearchUrl(query, start_date, end_date, debate_type) # Check if the dates are valid
        return [Debate(url) for url in self.getDebateUrls(query, start_date, end_date, debate_type)]

    def getDebateUrls(self, query: str, start_date: str = None, end_date: str = None, debate_type: DebateType = DebateType.ANY):
        done = False
        search_url = self.__checkAndGenerateSearchUrl(query, start_date, end_date, debate_type)

        while not done:
            soup = self.__getSoup(search_url)

            # Find all a href tags where the class is "video-thumb"
            debates = soup.find_all("a", {"class": "video-thumb"})
            debates = [self.base_url + debate["href"] for debate in debates]

            # Find the next page link, an a tag with the title "Ga naar volgende pagina"
            next_page = soup.find("a", {"title": "Ga naar volgende pagina"})

            if next_page:
                search_url = self.base_url + next_page["href"]
            else:
                done = True

        return debates