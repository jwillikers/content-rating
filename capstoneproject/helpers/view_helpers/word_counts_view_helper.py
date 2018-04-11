"""
This file provides helper functions for the word counts view.
"""
from django.contrib.auth.models import User
from capstoneproject.helpers import model_helper


def get_word_counts_context(user: User, pos: int):
    """
    This function creates the context dictionary to pass to the
    word counts page. The dictionary contains keys for the content
    title and for the category word counts dictionary.
    :param user: A User
    :param pos: An int, the position in the user's past rated
    content ordered where the most recent are at the top to
    retrieve word counts for
    :return: A dictionary
    """
    context = {'name': '',
               'category_word_counts': dict()
               }
    rating = model_helper.get_user_rating_at_position(user, pos)
    if not rating:
        return context
    context['name'] = rating.content.title
    context['category_word_counts'] = rating.get_word_count_category()
    return context
