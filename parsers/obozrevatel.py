"""Module for Obozrevatel site."""
import feedparser
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import urllib.request as ur
from config.logger import AppLogger


class SourceParser:
    """Main class for Obozrevatel site parser."""

    src = "https://www.obozrevatel.com/rss.xml"

    def __init__(self):
        """Init main class."""
        self.logger = AppLogger("parser_obozrevatel")

    def get_news(self):
        """Get new posts from current source."""
        d = feedparser.parse(self.src)
        news = []
        for n in d.entries:
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
        with ur.urlopen(link) as response:
            soup = BeautifulSoup(
                response.read(),
                "html.parser",
                from_encoding="cp1251"
            )
            text_div = soup.find("div", class_="news-full__text")
            if not text_div:
                text_div = soup.find("div", class_="news-video-full__text")
            if text_div:
                for script in text_div(["script", "style"]):
                    script.decompose()
                text = text_div.get_text()
            else:
                logger_message = "Can not find text block for URL {}".format(
                    link
                )
                self.logger.write_error(logger_message)
        return text
