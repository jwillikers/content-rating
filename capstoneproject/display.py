import capstoneproject.models as models
from django.db.models import Prefetch

def display_categories():
    return models.Category.objects.all()


def display_words():
    return models.Word.objects.all()

def display_all():
    words = models.Word.objects.prefetch_related('word_category_set__category')
    all = dict()
    for word in words:
        for word_category in word.word_category_set.all():
            word_category_dict = (
                {word.word:
                    {word_category.category.category:
                        (word_category.get_strength_display(), word_category.get_weight_display())}})
            all.update(word_category_dict)
    return all
