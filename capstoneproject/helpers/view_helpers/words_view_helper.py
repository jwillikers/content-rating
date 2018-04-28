"""
This file contains functions to help the words view.
"""
from django.contrib.auth.models import User
from capstoneproject.app_forms import WordsForm
from capstoneproject.helpers import model_helper
from capstoneproject.helpers.view_helpers import view_helper
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.models.content import Content
from capstoneproject.models.models.word_count import WordCount
from capstoneproject.models.models.category_rating import CategoryRating
from capstoneproject.models.fields.weight_field import WeightField


def get_words_context(user: User, category):
    """
    This function creates a context dictionary to provide the necessary
    data to the Words page.
    :param user: A User
    :param category: A string, the category name to whose word's are displayed
    :return: A dictionary, the context
    """
    weight_dict = view_helper.get_weight_dict()
    context = {'category': category,
               'words': model_helper.get_category_words(category_name=category),
               'weight_levels': len(weight_dict) - 1,
               'weight_dict': weight_dict,
               'words_form': WordsForm(category)
               }
    return context


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
    for word, weight in word_dict.items():
        x = model_helper.update_user_word_weight(user=request.user, word_name=word, category_name=category, weight=weight)
