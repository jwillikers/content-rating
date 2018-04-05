"""
This file contains functions used to provide data from the database to display on the UI.
"""
from capstoneproject.helpers import model_helper


def display_categories():
    """
    This function returns all categories that are used to classify offensive content.
    :return: A list of categories stored in the database.
    """
    return model_helper.get_categories()


def display_words():
    """
    This function returns all words that are used to classify offensive content.
    :return: A list of all words stored in the system's dictionary of offensive content.
    """
    return model_helper.get_words()


def display_category_words(category):
    """
    This function returns all words that are used to classify offensive content from the given category.
    :param category: The offensive category of words that should be returned.
    :return: A list of words in the given category stored in the system's dictionary of offensive content.
    """
    return model_helper.get_category_words(category)
