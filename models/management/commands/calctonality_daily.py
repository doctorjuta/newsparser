"""Console commands for calculating tonality."""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
import datetime
import sys
import pytz
from models.models import NewsMessage, NewsTonal, NewsTonalDaily


class Command(BaseCommand):
    """Main class for calculating daily tonality."""

    help = "Calculate tonality for news per days."

    def handle(self, *args, **options):
        """Run command."""
        today = datetime.datetime.now()
        tz = pytz.timezone(settings.TIME_ZONE)
        today = tz.localize(today)
        start_day = today - datetime.timedelta(days=1)
        start_day = start_day.replace(hour=0, minute=0, second=0)
        end_day = start_day.replace(hour=23, minute=59, second=59)
        all = NewsTonal.objects.all().filter(
            news_item__date__gt=start_day,
            news_item__date__lt=end_day
        ).order_by("news_item__date")
        if len(all) < 1:
            sys.exit("Emply news list")
        news_in_one_day = []
        for it in all:
            news_in_one_day.append(it.tonality_index)
        tonality_yesterday = self.get_tonality(news_in_one_day)
        tonality = 0
        if tonality_yesterday > 0:
            tonality = 1
        elif tonality_yesterday < 0:
            tonality = -1
        obj, created = NewsTonalDaily.objects.get_or_create(
            date=start_day
        )
        obj.tonality_index = tonality_yesterday
        obj.tonality = tonality
        obj.save()

    def get_tonality(self, list_of_tonalities):
        """Calculate avarage tonality from provided list."""
        val = 0
        if len(list_of_tonalities) < 1:
            return val
        for it in list_of_tonalities:
            val += it
        return round(val/len(list_of_tonalities), 2)
