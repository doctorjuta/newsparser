"""List of views for news parser."""
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz
from models.models import NewsTonal, NewsTonalDaily, NewsSource, Pages
from views.helpers import data_nomralize_tonality as dmt


class MainView(View):
    """CBV - base site with methods for all project."""

    def get_stat_data(self, data, source, prefix):
        """Get statistics data for tonalities."""
        positive = 0
        negative = 0
        neutral = 0
        filters = {}
        tz = pytz.timezone(settings.TIME_ZONE)
        if prefix == "today":
            today = datetime.datetime.combine(
                datetime.date.today(),
                datetime.datetime.min.time()
            )
            today = tz.localize(today)
            filters["news_item__date__gte"] = today
        if prefix == "yesterday":
            today = datetime.datetime.combine(
                datetime.date.today(),
                datetime.datetime.min.time()
            )
            today = tz.localize(today)
            yesterday = today-datetime.timedelta(days=1)
            filters["news_item__date__gte"] = yesterday
            filters["news_item__date__lt"] = today
        if prefix == "last24":
            today = tz.localize(datetime.datetime.today())
            yesterday = today-datetime.timedelta(days=1)
            filters["news_item__date__gte"] = yesterday
        if source:
            filters["news_item__source"] = source
        all = NewsTonal.objects.all().filter(
            **filters
        ).order_by(
            "news_item__date"
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
            if it.tonality_index > 0:
                positive += 1
            elif it.tonality_index < 0:
                negative += 1
            else:
                neutral += 1
        if len(all) > 0:
            avarage = round(avarage/len(all), 2)
        data["{}_count_positive".format(prefix)] = positive
        data["{}_count_negative".format(prefix)] = negative
        data["{}_count_neutral".format(prefix)] = neutral
        data["{}_count_all".format(prefix)] = len(all)
        data["{}_avarage_val".format(prefix)] = avarage
        data["{}_max_val".format(prefix)] = max_val
        data["{}_min_val".format(prefix)] = min_val
        return data


class HomePageView(MainView):
    """CBV for home page."""

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        """Home page - get request."""
        data = {}
        if request.user.is_authenticated:
            template_name = "home-login.html"
            data = self.get_stat_data(data, False, "today")
            data = self.get_stat_data(data, False, "yesterday")
        else:
            data = self.get_stat_data(data, False, "last24")
            template_name = "home-anonymous.html"
        return render(
            request,
            template_name,
            data
        )


class SingleSourcePage(MainView):
    """CBV for single source page (UA Pravda, RBC, etc)."""

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        """Single source page - get request."""
        data = {
            "title": "Джерело",
            "source_url": "",
            "source_id": "",
            "source_logo": "",
            "source_desc": ""
        }
        source = NewsSource.objects.get(pk=self.kwargs["id"])
        if source:
            data["title"] = source.name
            data["source_url"] = source.url
            data["source_id"] = source.id
            data["source_logo"] = source.logo
            data["source_desc"] = source.desctiption
        template_name = "single-source.html"
        data = self.get_stat_data(data, source, "today")
        return render(
            request,
            template_name,
            data
        )


class RESTAPIView(View):
    """CBV for REST API calls."""

    MAX_VAL = 100

    def post(self, request, *args, **kwargs):
        """REST API main request."""
        if "action" not in request.POST:
            return HttpResponseBadRequest(
                "Invalid arguments"
            )
        action = request.POST["action"]
        data = False
        if action == "tonality_charts":
            data = self.tonalityGeneral(request)
        if action == "tonality_daily":
            data = self.tonalityDaily(request)
        if action == "tonality_custom":
            data = self.tonalityCustom(request)
        if action == "tonality_daily_custom":
            data = self.tonalityDailyCustom(request)
        if data and "error" in data:
            return HttpResponseBadRequest(
                data["message"]
            )
        return JsonResponse({
            "data": data
        })

    def tonalityGeneral(self, request):
        """Return data for tonality by provided time range."""
        time = "today"
        source_id = False
        if "time" in request.POST:
            time = request.POST["time"]
        if "source_id" in request.POST:
            source_id = request.POST["source_id"]
        tz = pytz.timezone(settings.TIME_ZONE)
        today = datetime.date.today()
        if time == "yesterday":
            yesterday = today - datetime.timedelta(days=1)
            yesterday_time = datetime.datetime.combine(
                yesterday,
                datetime.datetime.min.time()
            )
            time = datetime.datetime.now() - datetime.timedelta(days=1)
            yesterday_time = tz.localize(yesterday_time)
            time = tz.localize(time)
            objs = NewsTonal.objects.all().filter(
                news_item__date__gte=yesterday_time,
                news_item__date__lt=time
            )
        else:
            time = datetime.datetime.combine(
                today,
                datetime.datetime.min.time()
            )
            time = tz.localize(time)
            objs = NewsTonal.objects.all().filter(
                news_item__date__gte=time
            )
        if source_id:
            objs = objs.filter(
                news_item__source__id=source_id
            )
        data = dmt(objs, self.MAX_VAL)
        return data[::-1]

    def tonalityDaily(self, request):
        """Return data for tonality dailty charts."""
        data = []
        start_day = datetime.datetime.now() - datetime.timedelta(days=30)
        tz = pytz.timezone(settings.TIME_ZONE)
        start_day = tz.localize(start_day)
        last_daily_tonality = NewsTonalDaily.objects.all().filter(
            date__gte=start_day
        ).order_by("date")
        for item in last_daily_tonality:
            data.append({
                "date": item.date,
                "tonality": item.tonality,
                "tonality_index": item.tonality_index
            })
        return data

    def tonalityCustom(self, request):
        """Return data for custom data range tonality."""
        data = []
        if "range" not in request.POST:
            return {
                "error": 1,
                "message": "Date range doesn't provide"
            }
        range = request.POST["range"].split(" - ")
        if len(range) < 2:
            return {
                "error": 1,
                "message": "Invalid date range"
            }
        start_day = datetime.datetime.strptime(
            range[0], "%Y-%m-%d %H:%M"
        )
        end_day = datetime.datetime.strptime(
            range[1], "%Y-%m-%d %H:%M"
        )
        tz = pytz.timezone(settings.TIME_ZONE)
        start_day = tz.localize(start_day)
        end_day = tz.localize(end_day)
        range_dates = end_day - start_day
        if (range_dates.days > 7):
            return {
                "error": 1,
                "message": "We provide data for maximum 7 days."
            }
        objs = NewsTonal.objects.all().filter(
            news_item__date__gt=start_day,
            news_item__date__lt=end_day
        )
        max_val_in_single = round(len(objs)/self.MAX_VAL)
        max_val_tonality = []
        max_val_index = []
        tmp_index = 1
        for item in objs.order_by("-news_item__date"):
            max_val_tonality.append(item.tonality)
            max_val_index.append(item.tonality_index)
            tmp_index += 1
            if tmp_index > max_val_in_single:
                data.append({
                    "news_title": item.news_item.title,
                    "news_date": item.news_item.date,
                    "tonality": round(
                        sum(max_val_tonality)/len(max_val_tonality), 2
                    ),
                    "tonality_index": round(
                        sum(max_val_index)/len(max_val_index), 2
                    )
                })
                max_val_tonality = []
                max_val_index = []
                tmp_index = 1
        return data

    def tonalityDailyCustom(self, request):
        """Return data for tonality dailty charts by custom date range."""
        data = []
        if "range" not in request.POST:
            return {
                "error": 1,
                "message": "Date range doesn't provide"
            }
        range = request.POST["range"].split(" - ")
        if len(range) < 2:
            return {
                "error": 1,
                "message": "Invalid date range"
            }
        start_day = datetime.datetime.strptime(
            range[0], "%Y-%m-%d %H:%M"
        )
        end_day = datetime.datetime.strptime(
            range[1], "%Y-%m-%d %H:%M"
        )
        tz = pytz.timezone(settings.TIME_ZONE)
        start_day = tz.localize(start_day)
        end_day = tz.localize(end_day)
        daily_tonality = NewsTonalDaily.objects.all().filter(
            date__gt=start_day,
            date__lt=end_day
        ).order_by("date")
        for item in daily_tonality:
            data.append({
                "news_date": item.date,
                "tonality": item.tonality,
                "tonality_index": item.tonality_index
            })
        return data


def page_about(request):
    """View for about page."""
    data = {
        "title": "Про проект",
        "text": ""
    }
    template_name = "page-about.html"
    try:
        about_page = Pages.objects.get(id=settings.ABOUT_PAGE_ID)
        data["title"] = about_page.title
        data["text"] = about_page.text
    except ObjectDoesNotExist:
        pass
    return render(
        request,
        template_name,
        data
    )


def page_custom_range(request):
    """View for custom range page."""
    data = {
        "title": "Тональність за обраний період часу"
    }
    template_name = "page-custom_range.html"
    return render(
        request,
        template_name,
        data
    )
