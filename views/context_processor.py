"""Additional context processors for project."""
from models.models import NewsSource


def addition_template_data(request):
    """Context processor for global menu."""
    site_title = "NewsDetect: аналізуємо тональність новин"
    site_name = "NewsDetect"
    sources = NewsSource.objects.all()
    return {
        "site_title": site_title,
        "site_name": site_name,
        "sources": sources
    }
