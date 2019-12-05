"""List of views for news parser."""
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz
from models.models import NewsTonal, NewsTonalDaily, NewsSource, Pages


class MainView(View):
    """CBV - base site with methods for all project."""

    def get_stat_data(self, date, data, source, prefix):
        """Get statistics data for tonalities."""
        positive = 0
        negative = 0
        neutral = 0
        filters = {}
        if isinstance(date, datetime.datetime):
            filters["news_item__date__gt"] = date
        else:
            filters["news_item__date__startswith"] = date
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
        data = {
            "title": _("Home page")
        }
        if request.user.is_authenticated:
            template_name = "home-login.html"
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            data = self.get_stat_data(today, data, False, "today")
            data = self.get_stat_data(yesterday, data, False, "yesterday")
        else:
            today_dt = datetime.datetime.today()
            yesterday_dt = today_dt - datetime.timedelta(days=1)
            data = self.get_stat_data(yesterday_dt, data, False, "last24")
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
            "title": _("Single source"),
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
        today = datetime.date.today()
        data = self.get_stat_data(today, data, source, "today")
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
                _("Invalid arguments")
            )
        action = request.POST["action"]
        data = False
        if action == "tonality_charts":
            data = self.tonalityGeneral(request)
        if action == "tonality_daily":
            data = self.tonalityDaily(request)
        if action == "tonality_custom":
            data = self.tonalityCustom(request)
        if data and "error" in data:
            return HttpResponseBadRequest(
                data["message"]
            )
        return JsonResponse({
            "data": data
        })

    def tonalityGeneral(self, request):
        """Return data for tonality by provided time range."""
        data = []
        time = "today"
        source_id = False
        if "time" in request.POST:
            time = request.POST["time"]
        if "source_id" in request.POST:
            source_id = request.POST["source_id"]
        today = datetime.date.today()
        if time == "yesterday":
            yesterday = today - datetime.timedelta(days=1)
            time = datetime.datetime.now() - datetime.timedelta(days=1)
            objs = NewsTonal.objects.all().filter(
                news_item__date__startswith=yesterday,
                news_item__date__lt=time
            )
        else:
            objs = NewsTonal.objects.all().filter(
                news_item__date__startswith=today
            )
        if source_id:
            objs = objs.filter(
                news_item__source__id=source_id
            )
        for item in objs.order_by("-news_item__date")[:self.MAX_VAL][::-1]:
            data.append({
                "news_title": item.news_item.title,
                "news_date": item.news_item.date,
                "tonality": item.tonality,
                "tonality_index": item.tonality_index
            })
        return data

    def tonalityDaily(self, request):
        """Return data for tonality dailty charts."""
        data = []
        start_day = timezone.now() - datetime.timedelta(days=30)
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
                "message": _("Date range doesn't provide")
            }
        range = request.POST["range"].split(" - ")
        if len(range) < 2:
            return {
                "error": 1,
                "message": _("Invalid date range")
            }
        start_day = datetime.datetime.strptime(
            range[0], "%Y-%m-%d %H:%M"
        )
        end_day = datetime.datetime.strptime(
            range[1], "%Y-%m-%d %H:%M"
        )
        timezone = pytz.timezone(settings.TIME_ZONE)
        start_day = timezone.localize(start_day)
        end_day = timezone.localize(end_day)
        range_dates = end_day - start_day
        if (range_dates.days > 7):
            return {
                "error": 1,
                "message": _("We provide data for maximum 7 days.")
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
                    "tonality": round(sum(max_val_tonality)/len(max_val_tonality), 2),
                    "tonality_index": round(sum(max_val_index)/len(max_val_index), 2)
                })
                max_val_tonality = []
                max_val_index = []
                tmp_index = 1
        return data


def page_about(request):
    """View for about page."""
    data = {
        "title": _("About project"),
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
        "title": _("Tonality for custom date range")
    }
    template_name = "page-custom_range.html"
    return render(
        request,
        template_name,
        data
    )
