"""Module for 112 Channel site."""
import feedparser
from datetime import datetime
import pytz
import urllib.request as ur
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from config.logger import AppLogger


class SourceParser:
    """Main class for 112 Channel site parser."""

    src = "https://ua.112.ua/rss/index.rss"

    def __init__(self):
        """Init main class."""
        self.logger = AppLogger("parser_channel112")

    def get_news(self):
        """Get new posts from current source."""
        d = feedparser.parse(self.src)
        news = []
        for n in d.entries:
            tz = pytz.timezone("UTC")
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
            text = self.get_news_text(n.link)
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
        req = ur.Request(
            link,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        try:
            with ur.urlopen(req) as response:
                soup = BeautifulSoup(
                    response.read(),
                    "html.parser",
                    from_encoding="utf8"
                )
                class_to_remove = [
                    "article-img",
                    "mob-show",
                    "mob-hide",
                    "article-tags",
                    "article-source"
                ]
                text_div = soup.find("div", class_="article-content_text")
                if not text_div:
                    text_div = soup.find("div", class_="post__text")
                if text_div:
                    for cls in class_to_remove:
                        for div in text_div.find_all("div", {"class": cls}):
                            div.decompose()
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
