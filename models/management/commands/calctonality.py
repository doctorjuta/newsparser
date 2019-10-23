"""Console commands for calculating tonality."""
from nltk.tokenize import word_tokenize
import string
import csv
from django.core.management.base import BaseCommand, CommandError
from models.models import NewsMessage, NewsTonal
from django.conf import settings

class Command(BaseCommand):
    """Main class for calculating tonality."""

    help = "Calculate tonality for news."

    def handle(self, *args, **options):
        """Run command."""
        new_items = NewsMessage.objects.filter(
            status="new"
        )[:20]
        if not new_items:
            return
        pos_neg_list = []
        pos_neg_val_list = []
        file_to_open = settings.BASE_DIR + "/tone-dict-uk.tsv"
        with open(file_to_open, "r", encoding="utf-8") as tsvfile:
            reader = csv.reader(tsvfile, delimiter="\t")
            for row in reader:
                pos_neg_list.append(row[0])
                pos_neg_val_list.append(row[1])
        stop_words = []
        file_to_open = settings.BASE_DIR + "/ukraine-stop-words.txt"
        with open(file_to_open, "r", encoding="utf-8") as file:
            for cnt, line in enumerate(file):
                stop_words.append(line.strip())
        for item in new_items:
            text = item.text.lower()
            text = text.replace("’", "").replace("'", "")
            text = text.translate(
                str.maketrans({key: None for key in string.punctuation})
            )
            word_tokens = word_tokenize(text)
            tonality_index = 0
            for w in word_tokens:
                if w in stop_words:
                    continue
                if w in pos_neg_list:
                    tonality_index += int(pos_neg_val_list[pos_neg_list.index(w)])
            obj, created = NewsTonal.objects.get_or_create(
                news_item=item
            )
            obj.tonality_index = tonality_index
            obj.tonality = 0
            if tonality_index > 0:
                obj.tonality = 1
            if tonality_index < 0:
                obj.tonality = -1
            obj.save()
            item.status = "completed"
            item.save()
