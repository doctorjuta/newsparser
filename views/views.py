"""List of views for news parser."""
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from models.models import NewsMessage, NewsTonal

class HomePageView(LoginRequiredMixin, View):
    """CBV for home page."""

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        """Home page - get request."""
        data = {
            "title": "Home page"
        }
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        data = self.get_data(today, data, "today")
        data = self.get_data(yesterday, data, "yesterday")
        return render(
            request,
            self.template_name,
            data
        )

    def get_data(self, date, data, prefix):
        """Simple wrapper for home request for getting data."""
        positive = NewsTonal.objects.all().filter(
            news_item__date__date=date,
            tonality_index__gte=0
        )
        negative = NewsTonal.objects.all().filter(
            news_item__date__date=date,
            tonality_index__lt=0
        )
        all = NewsTonal.objects.all().filter(
            news_item__date__date=datetime.date(2019, 10, 29)
        )
        avarage = 0
        max_val = 0
        min_val = 0
        for it in all:
            avarage += it.tonality_index
            if it.tonality_index > max_val:
                max_val = it.tonality_index
            if it.tonality_index < min_val:
                min_val = it.tonality_index
        if len(all) > 0:
            avarage = round(avarage/len(all), 2)
        data["{}_count_positive".format(prefix)] = len(positive)
        data["{}_count_negative".format(prefix)] = len(negative)
        data["{}_count_all".format(prefix)] = len(all)
        data["{}_avarage_val".format(prefix)] = avarage
        data["{}_max_val".format(prefix)] = max_val
        data["{}_min_val".format(prefix)] = min_val
        return data


class RESTAPIView(View):
    """CBV for REST API calls."""

    MAX_VAL = 100

    def post(self, request, *args, **kwargs):
        """REST API main request."""
        if "action" not in request.POST:
            return HttpResponseBadRequest(
                "Invalid arguments."
            )
        action = request.POST["action"]
        data = False
        if action == "tonality_charts":
            data = self.tonalityChart(request)
        return JsonResponse({
            "data": data
        })

    def tonalityChart(self, request):
        """Return data for charts."""
        data = []
        time = "today"
        if "time" in request.POST:
            time = request.POST["time"]
        today = datetime.date.today()
        if time == "yesterday":
            yesterday = today - datetime.timedelta(days = 1)
            objs = NewsTonal.objects.all().filter(
                news_item__date__date=yesterday
            ).order_by("news_item__date")[:self.MAX_VAL]
        else:
            objs = NewsTonal.objects.all().filter(
                news_item__date__startswith=today
            ).order_by("news_item__date")[:self.MAX_VAL]
        for item in objs:
            data.append({
                "news_title": item.news_item.title,
                "news_date": item.news_item.date,
                "tonality": item.tonality,
                "tonality_index": item.tonality_index
            })
        return data
