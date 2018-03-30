from django.core.management.base import BaseCommand
import capstoneproject.models as models


class Command(BaseCommand):
    def handle(self, *args, **options):
        ass = models.WordFeature.word_features.all()
        for result in ass:
            self.stdout.write(result.__str__())
