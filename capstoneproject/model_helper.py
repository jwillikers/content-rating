"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models import Category
from capstoneproject.models import Word
import traceback


def get_categories():
    """
    This function returns all categories that are used to classify offensive content.
    :return: A list of categories stored in the database.
    """
    return Category.categories.all()


def get_words():
    """
    This function returns all words that are used to classify offensive content.
    :return: A list of all words stored in the system's dictionary of offensive content.
    """
    return Word.words.all()


def get_category_words(category):
    """
    This function returns all words that are used to classify offensive content from the given category.
    :param category: The offensive category of words that should be returned.
    :return: A list of words in the given category stored in the system's dictionary of offensive content.
    """
    return Word.words.category(category)


def get_word(word):
    word_model = None
    try:
        word_model = Word.words.get_word(word=word)
    except TypeError:
        print(traceback.print_exc())
    return word_model
