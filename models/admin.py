from django.contrib import admin
from django.utils.html import format_html
from .models import NewsSource, NewsMessage, NewsTonal


admin.site.register(NewsSource)


@admin.register(NewsMessage)
class NewsMessageAdmin(admin.ModelAdmin):
    """Addition admin class for NewsMessage model."""

    ordering = ["-date"]


@admin.register(NewsTonal)
class NewsTonalAdmin(admin.ModelAdmin):
    """Addition admin class for NewsTonal model."""

    ordering = ["-news_item__date"]
    list_display = ("news_item", "news_tonal_column")

    def news_tonal_column(self, obj):
        """Show news tonal value in separate column."""
        color = "808080"
        tonality = int(obj.tonality)
        if tonality > 0:
            color = "00FF00"
        if tonality < 0:
            color = "FF0000"
        css = (
            "border-radius:50%;color:#fff;text-align:center;line-height:20px;"
            "display:block;width:20px;height:20px;background-color:#{};"
        ).format(
            color
        )
        return format_html(
            "<span style='{}'>{}</span>",
            css,
            obj.tonality_index
        )
    news_tonal_column.short_description = "Tonality"
