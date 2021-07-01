"""Module for Segodnya site."""
from datetime import datetime
import pytz
import json
from bs4 import BeautifulSoup
import urllib.request as ur
from urllib.error import HTTPError, URLError
from config.logger import AppLogger
from django.conf import settings


class SourceParser:
    """Main class for Segodnya site parser."""

    src = "https://www.segodnya.ua/data/last_news_uk.json"

    def __init__(self):
        """Init main class."""
        self.logger = AppLogger("parser_segodnya")

    def get_news(self):
        """Get new posts from current source."""
        json_data = []
        news = []
        try:
            req = ur.Request(
                self.src,
                data=None,
                headers={
                    'User-Agent': settings.USER_AGENT
                }
            )
            with ur.urlopen(req) as response:
                encoding = response.info().get_content_charset("utf-8")
                data = response.read()
                json_data = json.loads(data.decode(encoding))
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
        for n in json_data:
            link = n["path"]
            if "/uk/" in link:
                link = link.replace("/uk/", "/ua/")
            text = self.get_news_text(link)
            tz = pytz.timezone("UTC")
            date = datetime.fromtimestamp(n["timestamp"], tz=tz)
            news.append({
                "title": n["title"],
                "link": link,
                "date": date,
                "text": text
            })
        return news

    def get_news_text(self, link):
        """Get news text by provided link."""
        text = ""
        class_to_remove = [
            "content-more-links",
            "content-social",
            "article__share",
            "article__facebook",
            "article__footer",
            "article__banner-container",
            "article__time",
            "article__header",
            "article__author",
            "article__adml",
            "banner-img",
            "content-tags",
            "content-source",
            "content-footer-ads",
            "content-comments",
            "framebox",
            "content-meta"
        ]
        try:
            req = ur.Request(
                link,
                data=None,
                headers={
                    'User-Agent': settings.USER_AGENT
                }
            )
            with ur.urlopen(req) as response:
                soup = BeautifulSoup(
                    response.read(),
                    "html.parser"
                )
                if 'Project Shield Logo' in str(soup):
                    return ''
                text_div = soup.find("div", class_="article__body")
                if not text_div:
                    text_div = soup.find("div", class_="article-content")
                    if text_div:
                        text_div = text_div.find("div", class_="col-lg-8")
                if not text_div:
                    text_div = soup.find("article", class_="article__content")
                if not text_div:
                    text_div = soup.find("div", class_="article__content")
                if text_div:
                    for cls in class_to_remove:
                        for div in text_div.find_all("div", {"class": cls}):
                            div.decompose()
                    for script in text_div(["script", "style"]):
                        script.decompose()
                    text = text_div.get_text().strip()
                else:
                    message = "Can not find text block for URL {}".format(
                        link
                    )
                    self.logger.write_error(message)
        except URLError as e:
            message = "URLError with reason {}, URL: {}".format(
                e.reason,
                link
            )
            self.logger.write_error(message)
        except HTTPError as e:
            message = "HTTPError with code {} and reason {}".format(
                e.code,
                e.reason
            )
            self.logger.write_error(message)
        return text
