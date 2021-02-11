"""Module for Obozrevatel site."""
import feedparser
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import urllib.request as ur
from urllib.error import HTTPError, URLError
from config.logger import AppLogger


class SourceParser:
    """Main class for Obozrevatel site parser."""

    src = "https://www.obozrevatel.com/ukr/rss.xml"
    _headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "__cfduid=de9f8c28a02694a251da7cc160168a5941612981500; oboz_GDPRManager_userAnswer=eyJpc0FncmVlQW5hbHl0aWNzIjp0cnVlLCJpc0FncmVlRnVuY3Rpb25hbCI6dHJ1ZSwiaXNBZ3JlZU1hcmtldGluZyI6dHJ1ZSwiZGF0ZSI6IjIwMjEtMDItMTFUMTY6Mjc6NTMuOTA2WiJ9; oboz_GDPRManager_userAnswer_isAgreeMarketing=true; oboz_GDPRManager_userAnswer_isAgreeAnalytics=true; __tbc=%7Bjzx%7DRKlxRc9cNeAf6mVFg4i1HNS8SHf802M-USBlzHooNvCE-ARlcOqUuVhx3HvN1X_L2rwonuDDCSplqR4oimN_qyD5b4WocRDmMsCPdrMHMdE1YcA6INNNDOzoBdXNOAK7HvInHedgafemchY1LVQWow; __pat=7200000; __pvi=%7B%22id%22%3A%22v-2021-02-11-18-27-52-756-RH5WKNU7FJMCvtz0-0d5cccbfff50e93a481214d604ab1fe5%22%2C%22domain%22%3A%22.obozrevatel.com%22%2C%22time%22%3A1613061686993%7D; xbc=%7Bjzx%7DXhnnCWafjZ-AmCq53Rdjld_iM8ZmXTAUHVy6gpLGBeyXmiVLOzn9vnbb0kat0KKoEM43jIhN5of33u4X03YhRRHW3gbslpO2rDxvGL8YwCcVREHQaWm3DoF5ISCL8ehA8ny3OG-0GSsb5a3E6lxqyQ; pnespsdk_visitor=wz2hkfl2zz5sne06; pnespsdk_ssn=%7B%22%24s%22%3A1613060708121%2C%22visitNumber%22%3A3%7D",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }

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
        class_to_remove = [
            "footnote"
        ]
        request = ur.Request(
            link,
            None,
            self._headers,
            "https://obozrevatel.com"
        )
        try:
            with ur.urlopen(request) as response:
                soup = BeautifulSoup(
                    response.read(),
                    "html.parser",
                    from_encoding="cp1251"
                )
                text_div = soup.find("div", class_="newsFull_text")
                if not text_div:
                    text_div = soup.find("div", class_="news-video-full__text")
                if not text_div:
                    text_div = soup.find("div", class_="news-full__text")
                if not text_div:
                    text_div = soup.find("div", class_="newsItem_fullText")
                if text_div:
                    for cls in class_to_remove:
                        for div in text_div.find_all("div", {"class": cls}):
                            div.decompose()
                    for script in text_div(["script", "style"]):
                        script.decompose()
                    text = text_div.get_text()
                    if soup.original_encoding == 'cp1251':
                        text = text.encode('cp1251').decode('utf-8')
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
