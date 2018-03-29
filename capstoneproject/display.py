import capstoneproject.models as models
from django.db.models import Prefetch

def display_categories():
    return models.Category.objects.all()


def display_words():
    return models.Word.objects.all()

def display_words_info():
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
    return all
