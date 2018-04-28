"""
This file contains functions that provide help create the information displayed in the various views.
"""
import capstoneproject.content_rating.algorithm.text as text
from capstoneproject.shared import rater
from django.contrib.auth.models import User
from capstoneproject.helpers import model_helper
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.models.content import Content
from capstoneproject.models.models.word_count import WordCount
from capstoneproject.models.models.category_rating import CategoryRating
from capstoneproject.models.fields.weight_field import WeightField


def get_weight_dict():
    """
    This function creates a weight dictionary containing
    the numerical and string values associated with the
    possible weights.
    :return: A dictionary
    """
    weight_dict = dict()
    for weight in model_helper.get_weights():
        weight_dict[weight[0]] = weight[1]
    return weight_dict
