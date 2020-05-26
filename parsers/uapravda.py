"""Module for UA Pravda site."""
import feedparser
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import urllib.request as ur
from urllib.error import HTTPError, URLError
from config.logger import AppLogger


class SourceParser:
    """Main class for UA Pravda site parser."""

    src = "https://www.pravda.com.ua/rss/view_news/"

    def __init__(self):
        """Init main class."""
        self.logger = AppLogger("parser_uapravda")

    def get_news(self):
        """Get new posts from current source."""
        d = feedparser.parse(self.src)
        news = []
        for n in d.entries:
            if not n.link:
                continue
            tz = pytz.timezone("UTC")
            text = self.get_news_text(n.link)
            date = datetime(
                n.published_parsed[0],
                n.published_parsed[1],
                n.published_parsed[2],
                n.published_parsed[3],
                n.published_parsed[4],
                n.published_parsed[5],
                0,
                tz
            )
            news.append({
                "title": n.title,
                "link": n.link,
                "date": date,
                "text": text
            })
        return news

    def get_news_text(self, link):
        """Get news text by provided link."""
        text = ""
        try:
            with ur.urlopen(link) as response:
                soup = BeautifulSoup(
                    response.read(),
                    "html.parser",
                    from_encoding="cp1251"
                )
                text_div = soup.find("div", class_="post_news__text")
                if not text_div:
                    text_div = soup.find("div", class_="post__text")
                if not text_div:
                    text_div = soup.find("article", class_="article")
                if text_div:
                    for script in text_div(["script", "style"]):
                        script.decompose()
                    text = text_div.get_text()
                else:
                    message = "Can not find text block for URL {}".format(
                        link
                    )
                    self.logger.write_error(message)
        except URLError as e:
            message = "URLError with reason {}".format(
                e.reason
            )
            self.logger.write_error(message)
        except HTTPError as e:
            message = "HTTPError with code {} and reason {}".format(
                e.code,
                e.reason
            )
            self.logger.write_error(message)
        return text
