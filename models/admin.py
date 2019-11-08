from django.contrib import admin
from django.utils.html import format_html
from .models import NewsSource, NewsMessage, NewsTonal, NewsTonalDaily
from .models import Pages


admin.site.register(NewsSource)
admin.site.register(Pages)


@admin.register(NewsMessage)
class NewsMessageAdmin(admin.ModelAdmin):
    """Addition admin class for NewsMessage model."""

    ordering = ["-date"]


class TonalAdminBase(admin.ModelAdmin):
    """Abstract class for tonality."""

    def news_tonal_column(self, obj):
        """Show news tonal value in separate column."""
        color = "808080"
        tonality = int(obj.tonality)
        if tonality > 0:
            color = "00FF00"
        if tonality < 0:
            color = "FF0000"
        css = (
            "height:20px;display:inline-block;width:20px;margin-right:6px;"
            "border-radius:50%;background-color:#{};vertical-align:-5px;"
        ).format(
            color
        )
        return format_html(
            "<span style='{}'></span>{}",
            css,
            obj.tonality_index
        )

    news_tonal_column.short_description = "Tonality"


@admin.register(NewsTonalDaily)
class NewsTonalDailyAdmin(TonalAdminBase):
    """Addition admin class for NewsTonalDaily model."""

    ordering = ["-date"]
    list_display = ("date", "news_tonal_column")


@admin.register(NewsTonal)
class NewsTonalAdmin(TonalAdminBase):
    """Addition admin class for NewsTonal model."""

    ordering = ["-news_item__date"]
    list_display = ("news_item", "news_tonal_column")
