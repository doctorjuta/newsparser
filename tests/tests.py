"""Tests for parsers module."""
from django.test import TestCase
from unittest import skip
import datetime
from django.utils import timezone
from models.models import NewsSource
from parsers.main import MainParser


class TestParsers(TestCase):
    """Main class for parsers tests."""

    UA_PRAVDA_RSS_URL = "https://www.pravda.com.ua/rss/view_news/"

    def test_main_parser(self):
        """Test possibility to run main parsers script."""
        now = timezone.now()
        d = now - datetime.timedelta(minutes=20)
        for n in range(2):
            source = NewsSource.objects.create(
                name="Test Source {}".format(n),
                url=self.UA_PRAVDA_RSS_URL,
                parser="default"
            )
            source.last_parsed = d
            source.save()
        NewsSource.objects.create(
            name="Test Source 3",
            url=self.UA_PRAVDA_RSS_URL,
            parser="default"
        )
        parser = MainParser()
        parser.run()
        self.assertEqual(
            len(parser.sources),
            2
        )

    def test_ua_pravda_parser(self):
        """Test UA Pravda parser."""
        from models.models import NewsMessage
        now = timezone.now()
        d = now - datetime.timedelta(minutes=20)
        source = NewsSource.objects.create(
            name="UA Pravda Source",
            url=self.UA_PRAVDA_RSS_URL,
            parser="uapravda"
        )
        source.last_parsed = d
        source.save()
        parser = MainParser()
        parser.run()
        news = NewsMessage.objects.all()
        self.assertGreater(
            len(news),
            0
        )
