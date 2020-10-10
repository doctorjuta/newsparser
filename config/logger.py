"""Simple library for loggin process."""
import logging
from logging.handlers import RotatingFileHandler
from django.conf import settings
import requests


class AppLogger:
    """Logger main class."""

    LOGGER_FILE_INFO = settings.BASE_DIR + "/logs/info.log"
    LOGGER_NAME_INFO = "info"
    LOGGER_INFO = False

    LOGGER_FILE_ERRORS = settings.BASE_DIR + "/logs/errors.log"
    LOGGER_NAME_ERRORS = "errors"
    LOGGER_ERRORS = False

    MAX_BYTES = 10485760

    def __init__(self, logger_name=False):
        """Init class."""
        if logger_name:
            self.LOGGER_NAME_INFO = "{}_{}".format(
                self.LOGGER_NAME_INFO,
                logger_name
            )
            self.LOGGER_NAME_ERRORS = "{}_{}".format(
                self.LOGGER_NAME_ERRORS,
                logger_name
            )
        self.create_logger()

    def create_logger(self):
        """Create logger object."""
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        error_handler = RotatingFileHandler(
            self.LOGGER_FILE_ERRORS,
            maxBytes=self.MAX_BYTES,
            backupCount=5,
            encoding="utf8"
        )
        error_handler.setFormatter(formatter)
        self.LOGGER_ERRORS = logging.getLogger(self.LOGGER_NAME_ERRORS)
        self.LOGGER_ERRORS.setLevel(logging.ERROR)
        self.LOGGER_ERRORS.addHandler(error_handler)
        info_handler = RotatingFileHandler(
            self.LOGGER_FILE_INFO,
            maxBytes=self.MAX_BYTES,
            backupCount=5,
            encoding="utf8"
        )
        info_handler.setFormatter(formatter)
        self.LOGGER_INFO = logging.getLogger(self.LOGGER_NAME_INFO)
        self.LOGGER_INFO.setLevel(logging.INFO)
        self.LOGGER_INFO.addHandler(info_handler)

    def write_info(self, message):
        """Write information message."""
        self.LOGGER_INFO.info(message)

    def write_error(self, message):
        """Write error message."""
        self.LOGGER_ERRORS.error(message)
        telegram_message = "{}: {}".format("NEWS-DETECT", message)
        send_url = (
            "https://api.telegram.org/bot{}/sendMessage?"
            "chat_id={}&text={}"
        ).format(
            settings.TELEGRAM_BOT_TOKEN,
            settings.TELEGRAM_CHAT_ID,
            telegram_message
        )
        response = requests.post(send_url)
