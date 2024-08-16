"""
A module to fetch data from Brutalist.report website asynchronously, including topics, sources, posts, and last update time.

- `BrutalistFetch(connection_reuse: bool = False)` - Initializes a BrutalistFetch object with optional connection reuse. Connection reuse will work great with context manager else you have to manage the session life.
- `async fetch_feed_topics() -> dict` - Fetches a list of topics available from the Brutalist.report homepage.
- `async fetch_sources(topic: str = '') -> dict` - Fetches a list of available sources with optional given topic.
- `async fetch_source_posts(source_link: str, date: datetime.date, limit: int = POSTS_MAX_LIMIT) -> dict` - Fetches posts from a source by date, optionally filtering by limit.
- `async fetch_last_update_time() -> datetime.datetime` - Fetches the last update time from the Brutalist.report homepage.
- `async fetch_keyword_search() -> dict` - Fetches posts from Brutalist.report website based on a given keyword on specified date, optionally filtering by limit.
"""

import datetime

import aiohttp
from bs4 import BeautifulSoup

from ._constants import brutalist_home_url, POSTS_MAX_LIMIT
from ._helpers import extract_headlines, is_http_link


class BrutalistFetch():
    """
    A class to fetch data from Brutalist.report website.

    Connection reuse will work great with context manager else you have to manage the session life.
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
            self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connect_reuse:
            await self.session.close()

    async def __get_page(self, url: str) -> BeautifulSoup:
        """
        Fetches a web page and returns its BeautifulSoup representation.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the fetched web page.
        """
        if self.connect_reuse:
            async with self.session.get(url=url) as response:
                text = await response.text()
                return BeautifulSoup(text, "lxml")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return BeautifulSoup(await response.text(), "lxml")

    async def fetch_feed_topics(self) -> dict:
        """
        Fetches a list of topics from the Brutalist.report homepage.

        Returns:
            dict: A dictionary where keys are topic names (lowercase) and values are their corresponding URLs.
        """
        feed_topics = {}

        nav0 = (await self.__get_page(url=brutalist_home_url)).find_all("nav")[0]
        topics = nav0.find_all('a')[1:]

        feed_topics["topics"] = {topic.string.lower(): brutalist_home_url + topic["href"]
                                 for topic in topics if topic['href'].startswith("/topic")}

        return feed_topics

    async def fetch_sources(self, topic: str = '') -> dict:
        """
        Fetches a list of sources for a given topic.

        Args:
            topic (str, optional): The topic name or the topic URL to fetch sources for. Defaults to all topics available.

        Returns:
            dict: A dictionary where keys are source names and values are their corresponding URLs.
        """
        __is_http_link = is_http_link(link=topic)

        url = topic if __is_http_link else (
            brutalist_home_url + (f'/topic/{topic.lower()}' if topic else '') + '?limit=2')

        page = (await self.__get_page(url=url)).find_all("div", class_="brutal-grid")[0]

        sources = {
            "sources_fetched_from": url,
            "sources": {},
        }

        if topic:
            sources["topic"] = topic

        for source in page.find_all("h3"):
            a = source.find_all("a")[0]
            sources["sources"][a.string] = brutalist_home_url + a["href"]

        return sources

    async def fetch_source_posts(self, source: str, date: datetime.date, limit: int = POSTS_MAX_LIMIT) -> dict:
        """
        Fetches posts of a source from specific date, optionally filtering by limit (number of posts to retrieve).

        Args:
            source (str): The source name or the URL of the source to fetch posts from.
            date (datetime.date): The date to retrive respective dated posts from source.
            limit (int, optional): The maximum number of posts to fetch. Defaults to POSTS_MAX_LIMIT.

        Returns:
            dict: A dictionary containing the source name, source link, and a dictionary of posts where keys are post titles and values are their corresponding URLs.
        """
        content = {}
        date_not_today = date.strftime(
            "%Y-%m-%d") != datetime.date.today().strftime("%Y-%m-%d")

        __is_http_link = is_http_link(link=source)

        source_link = source if __is_http_link else (
            brutalist_home_url + "/source/" + source)

        if source_link.endswith("?"):
            source_link = source_link[:-1]

        if date_not_today:
            source_link += f'?before={date.strftime("%Y-%m-%d")}'

        if limit < POSTS_MAX_LIMIT:
            source_link += f"&limit={limit}" if date_not_today else f"?limit={limit}"

        source_page = await self.__get_page(url=source_link)
        brutal_grid = source_page.find_all("div", class_="brutal-grid")[0]

        content["source_name"] = brutal_grid.find_all("h3")[0].string
        content["source_link"] = source_link
        content["posts"] = extract_headlines(page=source_page)

        return content

    async def fetch_last_update_time(self) -> datetime.datetime:
        """
        Fetches the last update time in PT timezone from the Brutalist.report homepage.

        Returns:
            datetime.datetime: The last update time in PT timezone.
        """
        update_text = (await self.__get_page(
            url=brutalist_home_url)).find_all("aside")[0].string

        date_time_str = update_text.split("Last updated ")[1].split(" (")[0]

        return datetime.datetime.strptime(date_time_str, "%A, %B %d, %Y %H:%M %p")

    async def fetch_keyword_search(self, keyword: str, date: datetime.date, limit: int = POSTS_MAX_LIMIT) -> dict:
        """
        Fetches posts from Brutalist.report website based on a given keyword on specified date, optionally filtering by limit.

        Args:
            keyword (str): The keyword to search for.
            date (datetime.date): The date to filter posts by.
            limit (int, optional): The maximum number of posts to fetch. Defaults to POSTS_MAX_LIMIT.

        Returns:
            dict: A dictionary containing the keyword, and a dictionary of posts where keys are post titles and values are their corresponding URLs.
        """
        content = {}
        content["keyword"] = keyword

        date_not_today = date.strftime(
            "%Y-%m-%d") != datetime.date.today().strftime("%Y-%m-%d")

        __is_http_link = is_http_link(link=keyword)

        source_link = keyword if __is_http_link else (
            brutalist_home_url + "/keyword/" + keyword)

        if date_not_today:
            source_link += f'?before={date.strftime("%Y-%m-%d")}'

        if limit < POSTS_MAX_LIMIT:
            source_link += f"&limit={limit}" if date_not_today else f"?limit={limit}"

        keyword_results_page = await self.__get_page(url=source_link)
        content["posts"] = extract_headlines(page=keyword_results_page)
        content["keyword_search_url"] = source_link

        return content
