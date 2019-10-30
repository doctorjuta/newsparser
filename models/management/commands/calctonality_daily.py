"""Console commands for calculating tonality."""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import datetime
import sys
from models.models import NewsMessage, NewsTonal, NewsTonalDaily


class Command(BaseCommand):
    """Main class for calculating daily tonality."""

    help = "Calculate tonality for news per days."

    def handle(self, *args, **options):
        """Run command."""
        start_day = timezone.now() - datetime.timedelta(days=30)
        all = NewsTonal.objects.all().filter(
            news_item__date__gte=start_day
        ).order_by("news_item__date")
        if len(all) < 1:
            sys.exit("Emply news list")
        tonality_per_days = []
        actual_date = all[0].news_item.date.date()
        news_in_one_day = []
        for it in all:
            news_date = it.news_item.date.date()
            if news_date != actual_date:
                tonality_per_days.append({
                    "date": news_date,
                    "tonality_index": self.get_tonality(news_in_one_day)
                })
                actual_date = news_date
                news_in_one_day = []
            else:
                news_in_one_day.append(it.tonality_index)
        for it in tonality_per_days:
            tonality = 0
            if it["tonality_index"] > 0:
                tonality = 1
            elif it["tonality_index"] < 0:
                tonality = -1
            obj, created = NewsTonalDaily.objects.get_or_create(
                date=it["date"]
            )
            obj.tonality_index = it["tonality_index"]
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
