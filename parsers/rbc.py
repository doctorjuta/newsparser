"""Module for RBC site."""
import feedparser
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import os
from config.logger import AppLogger


class SourceParser:
    """Main class for RBC site parser."""

    src = "https://www.rbc.ua/static/rss/all.ukr.rss.xml"

    def __init__(self):
        """Init main class."""
        self.logger = AppLogger("parser_rbc")

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
            text = ""
            text_div = BeautifulSoup(n.fulltext, "html.parser")
            if text_div:
                for script in text_div(["script", "style"]):
                    script.decompose()
                text = text_div.get_text().strip()
                text = os.linesep.join([s for s in text.splitlines() if s])
            else:
                logger_message = "Can not find description for {}".format(
                    n.link
                )
                self.logger.write_error(logger_message)
            news.append({
                "title": n.title,
                "link": n.link,
                "date": date,
                "text": text
            })
        return news
