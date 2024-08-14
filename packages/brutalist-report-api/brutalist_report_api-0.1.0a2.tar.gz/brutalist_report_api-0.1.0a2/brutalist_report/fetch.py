"""
A module to fetch data from Brutalist.report website, including topics, sources, posts, and last update time.

- `BrutalistFetch(connection_reuse: bool = False)` - Initializes a BrutalistFetch object with optional connection reuse.
- `fetch_feed_topics() -> dict` - Fetches a list of topics available from the Brutalist.report homepage.
- `fetch_sources(topic: str = '') -> dict` - Fetches a list of available sources with optional given topic.
- `fetch_source_posts(source_link: str, date: datetime.date, limit: int = 50) -> dict` - Fetches posts from a source by date, optionally filtering by limit.
- `fetch_last_update_time() -> datetime.datetime` - Fetches the last update time from the Brutalist.report homepage.
"""

import datetime

import requests
from bs4 import BeautifulSoup

from ._constants import brutalist_home_url


class BrutalistFetch():
    """
    A class to fetch data from Brutalist.report website.
    
    Read about connection reuse here: https://stackoverflow.com/questions/24873927/python-requests-module-and-connection-reuse

    Args:
        connection_reuse (bool, optional): Set `True` of you want to reuse the already established connection/session/handshake with the website. Defaults to False.
    """

    def __init__(self, connection_reuse: bool = False) -> None:
        """
        Read about connection reuse here:
        https://stackoverflow.com/questions/24873927/python-requests-module-and-connection-reuse

        Args:
            connection_reuse (bool, optional): Set `True` of you want to reuse the already established connection/session/handshake with the website. Defaults to False.
        """
        self.connect_reuse = connection_reuse

        if connection_reuse:
            self.request = requests.Session()
        else:
            self.request = requests

    def __get_page(self, url: str) -> BeautifulSoup:
        """
        Fetches a web page and returns its BeautifulSoup representation.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the fetched web page.
        """
        return BeautifulSoup(self.request.get(url=url).text, "lxml")

    def __is_http_link(self, link: str) -> bool:
        return True if link.startswith("https://brutalist.report") else False

    def fetch_feed_topics(self) -> dict:
        """
        Fetches a list of topics from the Brutalist.report homepage.

        Returns:
            dict: A dictionary where keys are topic names (lowercase) and values are their corresponding URLs.
        """
        nav0 = self.__get_page(url=brutalist_home_url).find_all("nav")[0]
        topics = nav0.find_all('a')[1:]
        feed_topics = {topic.string.lower(): brutalist_home_url + topic["href"]
                       for topic in topics if topic['href'].startswith("/topic")}
        return feed_topics

    def fetch_sources(self, topic: str = '') -> dict:
        """
        Fetches a list of sources for a given topic.

        Args:
            topic (str, optional): The topic to fetch sources for. Defaults to all topics available.

        Returns:
            dict: A dictionary where keys are source names and values are their corresponding URLs.
        """
        is_http_link = self.__is_http_link(link=topic)
        url = topic if is_http_link else (
            brutalist_home_url + (f'/topic/{topic.lower()}' if topic else '') + '?limit=5')

        page = self.__get_page(url=url).find_all(
            "div", class_="brutal-grid")[0]

        sources = {
            "topic_link": url,
            "topic_name": page.find_all("h3")[0].string,
            "sources": {},
        }

        for source in page.find_all("h3"):
            a = source.find_all("a")[0]
            sources["sources"][a.string] = brutalist_home_url + a["href"]

        return sources

    def fetch_source_posts(self, source_link: str, date: datetime.date, limit: int = 50) -> dict:
        """
        Fetches posts of a source from specific date, optionally filtering by limit (number of posts to retrieve).

        Args:
            source_link (str): The URL of the source to fetch posts from.
            date (datetime.date): The date to retrive respective dated posts from source.
            limit (int, optional): The maximum number of posts to fetch. Defaults to 50.

        Returns:
            dict: A dictionary containing the source name, source link, and a dictionary of posts where keys are post titles and values are their corresponding URLs.
        """
        content = {}
        date_not_today = date.strftime(
            "%Y-%m-%d") != datetime.date.today().strftime("%Y-%m-%d")

        if source_link.endswith("?"):
            source_link = source_link[:-1]

        if date_not_today:
            source_link += f'?before={date.strftime("%Y-%m-%d")}'

        if limit < 50:
            source_link += f"&limit={limit}" if date_not_today else f"?limit={limit}"

        source_page = self.__get_page(url=source_link)
        brutal_grid = source_page.find_all("div", class_="brutal-grid")[0]

        content["source_name"] = brutal_grid.find_all("h3")[0].string
        content["source_link"] = source_link
        content["posts"] = {headline.find("a").string: headline.find_all("a")[0]["href"]
                            for headline in brutal_grid.find_all("ul")[0].find_all("li")}

        return content

    def fetch_last_update_time(self) -> datetime.datetime:
        """
        Fetches the last update time in PT timezone from the Brutalist.report homepage.

        Returns:
            datetime.datetime: The last update time in PT timezone.
        """
        update_text = self.__get_page(
            url=brutalist_home_url).find_all("aside")[0].string

        date_time_str = update_text.split("Last updated ")[1].split(" (")[0]

        return datetime.datetime.strptime(date_time_str, "%A, %B %d, %Y %H:%M %p")
