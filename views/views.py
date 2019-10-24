"""List of views for news parser."""
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
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
        if action == "charts":
            data = self.chartsRequest(request)
        if data:
            return JsonResponse({
                "data": data
            })
        else:
            return HttpResponseBadRequest(
                "Invalid action argument."
            )

    def chartsRequest(self, request):
        """Return data for charts."""
        if "model" not in request.POST:
            return False
        model = request.POST["model"]
        data = []
        if model == "news":
            objs = NewsMessage.objects.all()[:self.MAX_VAL]
            for item in objs:
                data.append({
                    "title": item.title,
                    "text": item.text,
                    "link": item.link,
                    "date": item.date,
                    "source": item.source.name
                })
        if model == "tonal":
            objs = NewsTonal.objects.all()[:self.MAX_VAL]
            for item in objs:
                data.append({
                    "news_title": item.news_item.title,
                    "tonality": item.tonality,
                    "tonality_index": item.tonality_index
                })
        return data
