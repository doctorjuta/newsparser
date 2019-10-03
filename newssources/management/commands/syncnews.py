"""Console commands for sync news in DB."""
from django.core.management.base import BaseCommand, CommandError
from parsers.main import MainParser

class Command(BaseCommand):
    """Main class for sync news in DB."""

    help = "Sync news in DB."

    def handle(self, *args, **options):
        """Run command."""
        parser = MainParser()
        parser.run()
