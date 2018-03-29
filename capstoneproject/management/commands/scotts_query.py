from django.core.management.base import BaseCommand
import capstoneproject.models as models

class Command(BaseCommand):
    def handle(self, *args, **options):
        # words = models.Word.objects.prefetch_related('word_category_set__category')
        words = models.get_words()
        all = dict()
        for word in words:
            word_all = dict()
            for word_category in word.word_category_set.all():
                category = word_category.category.category
                strength = word_category.get_strength_display()
                weight_numeric = word_category.weight
                weight_choice = word_category.get_weight_display()
                word_cat_dict = {category:
                                 {'strength': strength, 'weight': (weight_numeric, weight_choice)}}
                word_all.update(word_cat_dict)
            all.update({word: word_all})
        #for word in words:
            #self.stdout.write(all, style_func=None, ending=None)
            #self.stdout.write(word.__str__(), ending='\n')
            #for word_category in word.word_category_set.all():
            #    self.stdout.write('\t' + word_category.__str__(), style_func=None, ending=None)
