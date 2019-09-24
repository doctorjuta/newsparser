"""List of models for news parser."""
from django.db import models


class NewsSource(models.Model):
    """News source model."""

    PARSERS_DEFAULT = "default"
    PARSERS = [
        ("default", "Default"),
        ("default", "UA Pravda")
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
