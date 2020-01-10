"""Console commands for generate daily image with statistic info."""
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os


class Command(BaseCommand):
    """Main class for image generator command."""

    help = "Generate daily image with statistic info."
    font_bold_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "email",
        "fonts",
        "subset-RobotoCondensed-Bold.ttf"
    )
    font_regular_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "email",
        "fonts",
        "subset-RobotoCondensed-Regular.ttf"
    )
    logo_img_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "email",
        "img",
        "logo.png"
    )
    bg_color = "#E0E0E0"
    font_color = "#4A4A4A"

    def handle(self, *args, **options):
        """Run command."""
        main_img = Image.new("RGB", (640, 700), self.bg_color)
        logo_img = Image.open(self.logo_img_path)
        main_img.paste(logo_img, (30, 30))
        font_regular = ImageFont.truetype(
            self.font_regular_path,
            30
        )
        img = ImageDraw.Draw(main_img)
        img.text(
            (310, 41),
            "щоденний звіт:",
            font=font_regular,
            fill=self.font_color
        )
        img.line(
            (30, 100, 610, 100),
            fill=self.font_color
        )
        main_img.show()
