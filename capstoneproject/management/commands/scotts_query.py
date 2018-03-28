from django.core.management.base import BaseCommand
import capstoneproject.models as models

class Command(BaseCommand):
    def handle(self, *args, **options):
        words = models.Word.objects.prefetch_related('word_category_set__category')
        all = dict()
        for word in words:
            for word_category in word.word_category_set.all():
                word_category_dict = (
                    {word.word:
                        {word_category.category.category:
                            (word_category.get_strength_display(), word_category.get_weight_display())}})
                all.update(word_category_dict)

        self.stdout.write('displaying all:\n')
        for item in words:
            self.stdout.write(item.__str__(), ending='\n')
            for word_category in item.word_category_set.all():
                self.stdout.write('\t' + word_category.__str__(), style_func=None, ending=None)
