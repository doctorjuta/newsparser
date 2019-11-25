"""Additional context processors for project."""
from models.models import NewsSource


def menu_items(request):
    """Context processor for global menu."""
    sources = NewsSource.objects.all()
    return {
        "sources": sources
    }
