"""List of models for news parser."""
from django.db import models


class NewsSource(models.Model):
    """News source model."""

    PARSERS_DEFAULT = "default"
    PARSERS = [
        ("default", "Default"),
        ("uapravda", "UA Pravda"),
        ("obozrevatel", "Obozrevatel"),
        ("segodnya", "Segodnya"),
        ("ua24", "24 channel"),
        ("rbc", "RBC"),
        ("znaj", "Znaj")
    ]

    name = models.CharField(
        "Name",
        max_length=200
    )
    url = models.URLField(
        "Source main page URL",
        max_length=200
    )
    parser = models.CharField(
        "Parser",
        max_length=20,
        choices=PARSERS,
        default=PARSERS_DEFAULT
    )
    last_parsed = models.DateTimeField(
        "Last parsed",
        auto_now_add=True
    )

    def __str__(self):
        """Models item representation."""
        return self.name

    class Meta:
        """Addition data for model."""

        verbose_name = "Source"
        verbose_name_plural = "Sources"


class NewsMessage(models.Model):
    """Model for individual news message."""

    STATUS_DEFAULT = "new"
    STATUS_VARIANTS = [
        ("new", "New"),
        ("completed", "Completed")
    ]

    title = models.CharField(
        "Title",
        max_length=1000
    )
    text = models.TextField(
        "Text"
    )
    link = models.URLField(
        "Link",
        max_length=250
    )
    date = models.DateTimeField(
        "Date"
    )
    source = models.ForeignKey(
        "NewsSource",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        "Status",
        max_length=20,
        choices=STATUS_VARIANTS,
        default=STATUS_DEFAULT
    )

    def __str__(self):
        """Models item representation."""
        return "{}: {} / {}".format(self.source, self.title, self.date)

    class Meta:
        """Addition data for model."""

        verbose_name = "News item"
        verbose_name_plural = "News items"


class TonalityBase(models.Model):
    """Abstract class for all tonalities."""

    TONALITY_DEFAULT = 0
    TONALITY_VARIANTS = [
        (0, "Neutral"),
        (1, "Positive"),
        (-1, "Negative")
    ]

    tonality = models.IntegerField(
        "Tonality",
        choices=TONALITY_VARIANTS,
        default=TONALITY_DEFAULT
    )
    tonality_index = models.FloatField(
        "Tonality index",
        default=0.0
    )

    class Meta:
        """Addition data for model."""

        abstract = True


class NewsTonal(TonalityBase):
    """Model for news tonality."""

    news_item = models.ForeignKey(
        "NewsMessage",
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Models item representation."""
        return "{}".format(self.news_item)

    class Meta:
        """Addition data for model."""

        verbose_name = "Tonality"
        verbose_name_plural = "Tonalities"


class NewsTonalDaily(TonalityBase):
    """Summary tonality for every days."""

    date = models.DateField(
        "Date"
    )

    def __str__(self):
        """Models item representation."""
        return "{}: {}".format(self.date, self.tonality_index)

    class Meta:
        """Addition data for model."""

        verbose_name = "Daily tonality"
        verbose_name_plural = "Daily tonalities"
