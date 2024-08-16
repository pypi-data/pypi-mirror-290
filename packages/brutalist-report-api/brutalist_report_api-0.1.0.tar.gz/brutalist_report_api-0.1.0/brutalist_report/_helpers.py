from bs4 import BeautifulSoup

def is_http_link(link: str) -> bool:
    return True if link.startswith("https://brutalist.report") else False

def extract_headlines(page: BeautifulSoup) -> dict[str, str] | None:
    brutal_grid = page.find_all("div", class_="brutal-grid")[0]

    try:
        return {headline.find("a").string: headline.find_all("a")[0]["href"]
            for headline in brutal_grid.find_all("ul")[0].find_all("li")}
    except:
        return None
