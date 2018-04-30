"""
This file contains helper functions for the profile view
"""
from django.contrib.auth.models import User
from capstoneproject.app_forms \
    import ChangeUsernameForm, ChangePasswordForm, ChangeUsernamePasswordForm
from capstoneproject.helpers.view_helpers import view_helper
from capstoneproject.helpers.model_helpers import category_helper, rating_helper


def get_profile_context(user: User):
    """
    This function creates a context dictionary to provide the necessary
    data to the Profile page.
    :param user: A User
    :return: A dictionary, the context
    """
    weight_dict = view_helper.get_weight_dict()
    recently_rated = get_past_ratings_dict(user)
    print('\n\nUSER CATEGORIES ' + str(category_helper.get_user_categories(user)))
    context = {'categories': category_helper.get_user_categories(user),
               'recently_rated': recently_rated,
               'weight_levels': len(weight_dict) - 1,
               'weight_dict': weight_dict,
               'change_username_form': ChangeUsernameForm(),
               'change_password_form': ChangePasswordForm(),
               'change_username_password_form': ChangeUsernamePasswordForm()}
    return context


def get_past_ratings_dict(user: User):
    """
    This function creates a dictionary containing information on the user's
    past ratings.
    :param user: A User
    :return: A dict
    """
    recently_rated = dict()
    past_ratings = rating_helper.get_user_ratings(user)
    print("\n\nPAST RATINGS")
    print(past_ratings)
    for count, r in enumerate(past_ratings):
        title = '{} - {}'.format(count+1, r.content.title)
        recently_rated[title] = r.rating
    return recently_rated


def create_category_dictionary(post):
    """
    This function creates a dictionary from an HTTP Request Post
    that contains category names as keys and their weights as values.
    :param post: A dict, the POST from the HTTP Request
    :return: A dict
    """
    cat_dict = dict()
    for key, value in post.items():
        if key.endswith('_cat'):
            cat_dict[key[:-4]] = value
    return cat_dict


def update_user_category_weights(request):
    """
    This function updates the weights associated with the user's
    category weight values.
    :param request: An HTTP Request
    :return: None
    """
    cat_dict = create_category_dictionary(request.POST)
    for cat, weight in cat_dict.items():
        category_helper.update_user_category_weight(user=request.user, category_name=cat, weight=weight)
