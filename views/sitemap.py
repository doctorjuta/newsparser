"""List of views for sitemap."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime
from models.models import NewsSource


class StaticPagesSitemap(Sitemap):
    """Sitemap class form static pages."""

    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["home_page", "about", "custom_range"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return datetime(2019, 11, 24)


class SourcesSitemap(Sitemap):
    """Sitemap class form sources single pages."""

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return NewsSource.objects.all()

    def location(self, obj):
        return "/source/{}/".format(obj.pk)

    def lastmod(self, obj):
        return datetime(2019, 12, 19)
