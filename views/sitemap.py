"""List of views for sitemap."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from models.models import NewsSource


class StaticPagesSitemap(Sitemap):
    """Sitemap class form static pages."""

    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["home_page", "about", "custom_range"]

    def location(self, item):
        return reverse(item)


class SourcesSitemap(Sitemap):
    """Sitemap class form sources single pages."""

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return NewsSource.objects.all()

    def location(self, obj):
        return "/source/{}/".format(obj.pk)
