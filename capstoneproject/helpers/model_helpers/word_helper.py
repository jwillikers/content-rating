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
    This function returns all words that are used to classify offensive content.
    :return: A list of all words stored in the system's dictionary of offensive content.
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
    This function returns all words that are used to classify offensive content from the given category.
    :param category_name: The offensive category of words that should be returned.
    :param user: a User
    :return: A list of words in the given category stored in the system's dictionary of offensive content.
    """
    # print("\n\nUSER WORDS IN CATEGORY")
    # print(Word.words.category(category_name).filter(user_storage__user_id=user))
    return Word.words.category(category_name).filter(user_storage__user_id=user).order_by('name')


def get_user_word_features(user: User, word: str):
    """
    This function returns all word features associated with the given word and user.
    :param user: A User
    :param word: A string, the name of a word
    :return: A queryset of all word features associated with the word and user.
    """
    return Word.words.get(name=word).word_features.filter(user_storage__id=user.id)


def get_word_weight(user: User, word_name: str, category_name: str):
    """
    This function provides the weight associated with a given User, Word, and Category.
    If the user has stored their own word weight, then this value is returned.
    Otherwise, return the default word weight.
    :param user: A User
    :param word_name: A string, the word name
    :param category_name: A string, the category name
    :return: An int, the offensiveness weight associated with the given user, word, and category
    """
    return Word.words.get(name=word_name).word_features.get(
        user_storage__id=user.id, category__name=category_name).weight


def update_user_word_weight(user: User, word_name: str, category_name: str, weight: int):
    """
    This function updates the weight associated with the WordFeature of the given
    word and given category to be the given weight.
    :param user: A User
    :param word_name: A string, the word name
    :param category_name: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """

    # Get the WordFeature associated with the word and that category name.
    # If this is already in the UserStorage WordFeature list, stop.
    current_user_word_feature = Word.words.get(name=word_name).word_features.get(
        user_storage__id=user.id,
        category__name=category_name)
    if weight == current_user_word_feature.weight:
        return
    # Remove the old WordFeature for the given word and category from the UserStorage WordFeature list.
    #UserStorage.word_features.remove(current_user_word.word_features)
    # If no WordFeature with the category name and weight do not exist, create it.
    # Add the new WordFeature for the given word, category, weight to the UserStorage WordFeature list.
    #UserStorage.words.add(Word.words.get(name=word_name).word_features.get_or_create(user_storage__id=user.id,
    #                                                                                 category__name=category_name,
    #                                                                                 weight=weight))

    # TODO Change this
    # Get the user's storage
    user_query = UserStorage.user_storage.get(user=user.id)
    print("\n\nUSER QUERY: " + str(user_query))
    print("\n\nALL USER WORD FEATURES: " + str(user_query.word_features.all()))
    # Remove the old word feature
    user_query.word_features.remove(current_user_word_feature)

    # Get or create category matching name and weight.
    new_word_feature, created = Word.words.get(name=word_name).word_features.get_or_create(category=category_name,
                                                               strength=current_user_word_feature.strength,
                                                               weight=int(weight))
    print("NEW_WORD_FEATURE: " + str(new_word_feature))
    print(created)
    # Link the user's storage to the new category.
    #if created:
        #user_query.categories.add(new_cat)
    print('\n\nNEW ALL USER WORDS')
    print(user_query.word_features.all())
