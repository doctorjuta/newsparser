"""Console commands for sending regulat information to social channels."""
from django.core.management.base import BaseCommand
from django.conf import settings
from config.logger import AppLogger
import requests
import datetime
import os
import tweepy


class Command(BaseCommand):
    """Main class for sending information."""

    help = "Send some usefull regular information to social channels."

    def handle(self, *args, **options):
        """Run command."""
        self.img_path = self.get_image()
        if not self.img_path:
            return ""
        # self.post_to_twitter();
        self.post_to_telegram();

    def get_image(self):
        """Getting image with statistic information."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        self.img_caption = "Статистика за {}".format(date)
        img_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "infograph",
            "results",
            "{}.png".format(date)
        )
        if not os.path.isfile(img_path):
            return False
        return img_path

    def post_to_twitter(self):
        """Posting to Twitter."""
        tw_logger = AppLogger("twitter_api")
        auth = tweepy.OAuthHandler(
            settings.TW_CONSUMER_KEY,
            settings.TW_CONSUMER_SECRET
        )
        auth.set_access_token(
            settings.TW_ACCESS_TOKEN,
            settings.TW_ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)
        try:
            api.verify_credentials()
        except Exception as e:
            logger_message = "Error creating API."
            self.logger.write_error(logger_message)
            return ""
        result = api.update_with_media(
            filename=self.img_path,
            status=self.img_caption
        )
        print(result)

    def post_to_telegram(self):
        """Posting to Telegram."""
        with open(self.img_path, "rb") as img:
            files = {
                "photo": img
            }
            send_url = (
                "https://api.telegram.org/bot{}/sendPhoto?"
                "chat_id={}&parse_mode=Markdown&caption={}"
            ).format(
                settings.TG_BOT_TOKEN,
                settings.TG_CHAT_ID,
                self.img_caption
            )
            response = requests.post(send_url, files=files)
