from django.core.management.base import BaseCommand
import capstoneproject.models as models
from django.db.models import Prefetch



class Command(BaseCommand):
    def handle(self, *args, **options):
        category = 'excretory'

        words = models.Word.words.category(category)

        for word in words:
            self.stdout.write(word.__str__())
            self.stdout.write(word.word_features_list.__str__())
