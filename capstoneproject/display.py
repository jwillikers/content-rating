from capstoneproject.models import Category
from capstoneproject.models import Word


def display_categories():
    return Category.categories.all()


def display_words():
    return Word.words.all()


def display_category_words(category):
    return Word.words.category(category)
