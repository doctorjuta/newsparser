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
        return render(
            request,
            self.template_name,
            {
                "title": "Home page"
            }
        )


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
            )[:self.MAX_VAL]
        else:
            objs = NewsTonal.objects.all().filter(
                news_item__date__startswith=today
            )[:self.MAX_VAL]
        for item in objs:
            data.append({
                "news_title": item.news_item.title,
                "news_date": item.news_item.date,
                "tonality": item.tonality,
                "tonality_index": item.tonality_index
            })
        return data
