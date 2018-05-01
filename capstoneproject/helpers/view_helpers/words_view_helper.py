"""
This file contains functions to help the words view.
"""
from django.contrib.auth.models import User
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.word_feature import WordFeatureQuerySet
from capstoneproject.models.models.category import Category
from capstoneproject.helpers.view_helpers import view_helper
from capstoneproject.helpers.model_helpers import word_helper
from capstoneproject.helpers.model_helpers import category_helper


def get_words_context(user: User, category):
    """
    This function creates a context dictionary to provide the necessary
    data to the Words page.
    :param user: A User
    :param category: A string, the category name to whose word's are displayed
    :return: A dictionary, the context
    """
    weight_dict = view_helper.get_weight_dict()
    # print("\nCATEGORY: " + str(category))
    context = {'category': category,
               'words': create_user_word_dictionary(user, category),
               'weight_levels': len(weight_dict) - 1,
               'weight_dict': weight_dict
               }
    return context


def create_user_word_dictionary(user: User, category):
    """
    This method creates a dictionary containing the words
    associated with a user's category and the word weights.
    :param user: a User
    :param category: a string, the category name
    :return: a dictionary with word names as the keys and word weights as the values.
    """
    word_dict = {}
    words = word_helper.get_user_category_words(category_name=category, user=user)
    for word in words:
        word_dict[word.name] = word.word_features.get(
            user_storage__user_id=user.id,
            category=category_helper.get_default_category(category_name=category)).weight
    # print('\n\n' + str(word_dict))
    return word_dict


def create_word_weight_dictionary(post):
    """
    This function creates a word weight dictionary whose keys are
    word names and the values are word weights.
    :param post: A dict, the Post dictionary from an HTTP Request
    :return: A dict, containing word names and associated word weights
    """
    word_dict = dict()
    for key, value in post.items():
        key = ''
        if key.startswith('word_'):
            word_dict[key[5:]] = value
    return word_dict


def update_user_word_weights(request, category):
    """
    This function updates a user's word weights
    :param request: An HTTP Request
    :param category: A string, the category name whose words are being updated.
    :return: None
    """
    word_dict = create_word_weight_dictionary(request.POST)
    # print("\n\nWORD DICT: " + str(word_dict))
    for word, weight in word_dict.items():
        word_helper.update_user_word_weight(user=request.user, word_name=word, category_name=category, weight=weight)
