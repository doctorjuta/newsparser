"""Module for TSN site."""
import feedparser
from datetime import datetime
import pytz
from config.logger import AppLogger


class SourceParser:
    """Main class for TSN site parser."""

    src = "https://tsn.ua/rss/full.rss"

    def __init__(self):
        """Init main class."""
        self.logger = AppLogger("parser_tsn")

    def get_news(self):
        """Get new posts from current source."""
        d = feedparser.parse(self.src)
        news = []
        for n in d.entries:
            if not hasattr(n, 'link'):
                continue
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
            news.append({
                "title": n.title,
                "link": n.link,
                "date": date,
                "text": n.fulltext
            })
        return news
