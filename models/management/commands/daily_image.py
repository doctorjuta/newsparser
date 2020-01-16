"""Console commands for generate daily image with statistic info."""
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
from models.models import NewsTonalDaily, NewsTonal
import datetime
import pytz
import matplotlib
import matplotlib.pyplot as plt


class Command(BaseCommand):
    """Main class for image generator command."""

    help = "Generate daily image with statistic info."
    font_bold_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "infograph",
        "fonts",
        "subset-RobotoCondensed-Bold.ttf"
    )
    font_regular_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "infograph",
        "fonts",
        "subset-RobotoCondensed-Regular.ttf"
    )
    logo_img_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "infograph",
        "img",
        "logo.png"
    )
    bg_color = "#E0E0E0"
    font_color = "#4A4A4A"

    def handle(self, *args, **options):
        """Run command."""
        last_tonality = NewsTonalDaily.objects.last()
        all_tonalities = NewsTonal.objects.filter(
            news_item__date__startswith=last_tonality.date
        )
        fin_img_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "infograph",
            "results",
            "{}.png".format(last_tonality.date)
        )
        if os.path.isfile(fin_img_path):
            return ""
        main_img = Image.new("RGB", (640, 950), self.bg_color)
        logo_img = Image.open(self.logo_img_path)
        main_img.paste(logo_img, (30, 30))
        font_title = ImageFont.truetype(
            self.font_regular_path,
            26
        )
        font_regular = ImageFont.truetype(
            self.font_regular_path,
            20
        )
        font_footer = ImageFont.truetype(
            self.font_regular_path,
            14
        )
        img = ImageDraw.Draw(main_img)
        img.line(
            (30, 100, 610, 100),
            fill=self.font_color
        )
        positive = 0
        negative = 0
        neutral = 0
        for it in all_tonalities:
            if it.tonality_index > 0:
                positive += 1
            elif it.tonality_index < 0:
                negative += 1
            else:
                neutral += 1
        img.text(
            (330, 43),
            "{}".format(last_tonality.date),
            font=font_title,
            fill=self.font_color
        )
        img.text(
            (30, 130),
            "Статистика:",
            font=font_title,
            fill=self.font_color
        )
        img.text(
            (30, 180),
            "Загальна тональність: {}".format(last_tonality.tonality_index),
            font=font_regular,
            fill=self.font_color
        )
        img.text(
            (30, 210),
            "Кількість позитивних новин: {}".format(positive),
            font=font_regular,
            fill=self.font_color
        )
        img.text(
            (30, 240),
            "Кількість негативних новин: {}".format(negative),
            font=font_regular,
            fill=self.font_color
        )
        img.text(
            (30, 270),
            "Кількість нейтральних новин: {}".format(neutral),
            font=font_regular,
            fill=self.font_color
        )
        img.text(
            (30, 330),
            "Динаміка за останні 30 днів:",
            font=font_title,
            fill=self.font_color
        )
        path_to_chart = self.generate_new_daily_graph()
        chart_img = Image.open(path_to_chart)
        wpercent = (580/float(chart_img.size[0]))
        hsize = int((float(chart_img.size[1])*float(wpercent)))
        chart_img = chart_img.resize((580, hsize), Image.ANTIALIAS)
        main_img.paste(chart_img, (30, 390))
        img.line(
            (30, 880, 610, 880),
            fill=self.font_color
        )
        img.text(
            (30, 900),
            "Більше інформації на сайті news-detect.org.",
            font=font_footer,
            fill=self.font_color
        )
        main_img.save(fin_img_path)

    def generate_new_daily_graph(self):
        """Generate image with tonality for recent 30 days."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        path_to_img = os.path.join(
            settings.BASE_DIR,
            "static",
            "infograph",
            "charts",
            "daily",
            "{}.png".format(date)
        )
        if os.path.isfile(path_to_img):
            return path_to_img
        x_val = []
        y_val = []
        start_day = datetime.datetime.now() - datetime.timedelta(days=30)
        tz = pytz.timezone(settings.TIME_ZONE)
        start_day = tz.localize(start_day)
        last_daily_tonality = NewsTonalDaily.objects.all().filter(
            date__gte=start_day
        ).order_by("date")
        for item in last_daily_tonality:
            x_val.append("{}/{}".format(item.date.month, item.date.day))
            y_val.append(item.tonality_index)

        fig, ax = plt.subplots()
        ax.plot(x_val, y_val)
        ax.set(
            xlabel="",
            ylabel="",
            title="",
            facecolor="#E0E0E0",
            xmargin=0.1,
            ymargin=0.1
        )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid()
        plt.xticks(rotation=90)
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        fig.savefig(path_to_img, facecolor="#E0E0E0", bbox_inches="tight", pad_inches=0)
        return path_to_img
