"""Parsers library."""
import importlib
import datetime
from django.utils import timezone
from config.logger import AppLogger


class MainParser:
    """Main class for all prasers."""

    sources = []

    def run(self):
        """Init main class."""
        self.logger = AppLogger("parser_main")
        self.get_sources()
        self.get_news()

    def get_sources(self):
        """Get sources to parse."""
        from models.models import NewsSource
        now = timezone.now()
        d = now - datetime.timedelta(minutes=10)
        self.sources = NewsSource.objects.filter(
            last_parsed__lt=d
        )
        # self.sources = NewsSource.objects.all()

    def get_news(self):
        """Load module for parsing and scrape news."""
        from models.models import NewsMessage
        for s in self.sources:
            import_module = "parsers.{}".format(s.parser)
            try:
                parser_mod = importlib.import_module(
                    import_module
                )
            except ImportError:
                logger_message = "Can not import module {}".format(
                    import_module
                )
                self.logger.write_error(logger_message)
                parser_mod = False
            if not parser_mod or parser_mod.__name__ == "parsers.default":
                continue
            parser = parser_mod.SourceParser()
            news = parser.get_news()
            for n in news:
                obj, created = NewsMessage.objects.get_or_create(
                    title=n["title"],
                    link=n["link"],
                    date=n["date"],
                    source=s
                )
                if created:
                    obj.text = n["text"]
                    obj.save()
            now = timezone.now()
            s.last_parsed = now
            s.save()
            logger_message = "Finished for {} on {}".format(
                s.name,
                now
            )
            self.logger.write_info(logger_message)
