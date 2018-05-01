"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.user_storage import UserStorage
from django.contrib.auth.models import User
import traceback


def get_default_words():
    """
    This function returns all words that are used to
    classify offensive content.
    :return: A list of all words stored in the system's
    dictionary of offensive content.
    """
    return Word.words.filter(default=True)


def get_word(word_name: str):
    """
    Gets a Word model that matches the given string.
    :param word_name: A string, the word name to get.
    :return: A Word
    """
    word_model = None
    try:
        word_model = Word.words.get_word(word=word_name)
    except TypeError:
        print(traceback.print_exc())
    return word_model


def get_user_category_words(category_name, user: User):
    """
    This function returns all words that are used to
    classify offensive content from the given category.
    :param category_name: The offensive category of words
    that should be returned.
    :param user: a User
    :return: A list of words in the given category stored in
    the system's dictionary of offensive content.
    """
    return Word.words.category(category_name).filter(
        user_storage__user_id=user).order_by('name')


def get_user_word_features(user: User, word: str):
    """
    This function returns all word features associated with
    the given word and user.
    :param user: A User
    :param word: A string, the name of a word
    :return: A queryset of all word features associated with the word and user.
    """
    return Word.words.get(name=word).word_features.filter(
        user_storage__id=user.id)


def get_word_weight(user: User, word_name: str, category_name: str):
    """
    This function provides the weight associated with a
    given User, Word, and Category.
    If the user has stored their own word weight, then this value is returned.
    Otherwise, return the default word weight.
    :param user: A User
    :param word_name: A string, the word name
    :param category_name: A string, the category name
    :return: An int, the offensiveness weight associated
    with the given user, word, and category
    """
    return Word.words.get(name=word_name).word_features.get(
        user_storage__id=user.id, category__name=category_name).weight


def update_user_word_weight(
        user: User,
        word_name: str,
        category_name: str,
        weight: int):
    """
    This function updates the weight associated with the \
    WordFeature of the given
    word and given category to be the given weight.
    :param user: A User
    :param word_name: A string, the word name
    :param category_name: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """

    word_feature = WordFeature.word_features.get(
            user_storage__id=user.id,
            words__name=word_name,
            category__name=category_name)
    if weight == word_feature.weight:
        return
    else:
        strength = word_feature.strength
        word_feature.delete()
        WordFeature.word_features.get_or_create(
            category__name=category_name,
            strength=strength,
            weight=weight)
        user_storage = UserStorage.user_storage.get(id=user.id)
        user_storage.word_feature.add(word_feature)
        user_storage.save()
