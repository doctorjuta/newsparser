"""Console commands for sending regulat information to social channels."""
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import datetime
import os


class Command(BaseCommand):
    """Main class for sending information."""

    help = "Send some usefull regular information to social channels."

    def handle(self, *args, **options):
        """Run command."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        img_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "infograph",
            "results",
            "{}.png".format(date)
        )
        if not os.path.isfile(img_path):
            return ""
        with open(img_path, "rb") as img:
            files = {
                "photo": img
            }
            img_caption = "Статистика за {}".format(date)
            send_url = (
                "https://api.telegram.org/bot{}/sendPhoto?"
                "chat_id={}&parse_mode=Markdown&caption={}"
            ).format(
                settings.TG_BOT_TOKEN,
                settings.TG_CHAT_ID,
                img_caption
            )
            response = requests.post(send_url, files=files)
