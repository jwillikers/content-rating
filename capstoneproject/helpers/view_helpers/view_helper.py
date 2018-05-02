"""
This file contains functions that provide help create the information displayed in the various views.
"""
from capstoneproject.helpers.model_helpers import model_helper


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
