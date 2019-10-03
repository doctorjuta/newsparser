from django.contrib import admin
from .models import NewsSource, NewsMessage


admin.site.register(NewsSource)

@admin.register(NewsMessage)
class NewsMessageAdmin(admin.ModelAdmin):
    """Addition admin class for NewsMessage model."""

    ordering = ["-date"]
