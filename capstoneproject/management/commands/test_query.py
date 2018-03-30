from django.core.management.base import BaseCommand
import capstoneproject.models as models


class Command(BaseCommand):
    def handle(self, *args, **options):
        ass = models.Word.words.get_word('ass')
        self.stdout.write(ass.__str__())
        #for result in ass:
        #    self.stdout.write(result.__str__())
