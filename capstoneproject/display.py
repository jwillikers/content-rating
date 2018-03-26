import capstoneproject.models as models


def display_categories():
    return models.Category.objects.all()


def display_words():
    return models.Word.objects.all()
