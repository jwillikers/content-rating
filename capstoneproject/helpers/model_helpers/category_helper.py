"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.user_storage import UserStorage
from django.contrib.auth.models import User


def get_default_categories():
    """
    This function returns all categories that are used to classify offensive content.
    :return: A list of categories stored in the database.
    """
    return Category.categories.filter(default=True).order_by('name')


def get_default_category(category_name):
    """
    This function returns a Category that matches the given category name.
    :param category_name: A string, the category name
    :return: A Category
    """
    return Category.categories.get(name=category_name, default=True)


def get_user_categories(user: User):
    """
    Retrieves a User's Categories.
    :param user: A User
    :return: A list of a User's Categories
    """
    return Category.categories.filter(user_storage__id=user.id).order_by('name')


def get_user_category(user: User, category_name: str):
    """
    This function returns a Category model associated with
    the given User and category name.
    :param user: A User
    :param category_name: A string, the name of the category
    :return: A Category model
    """
    return Category.categories.get(name=category_name, user_storage__id=user.id)


def get_num_default_categories():
    """
    This function returns the number of unique category names identified by the system.
    :return: An int
    """
    return len(get_default_categories())


def get_user_category_weight(user: User, category_name: str):
    """
    This function provides the weight associated with a given User and Category.
    If the user has stored their own category weight, then this value is returned.
    Otherwise return the default category weight.
    :param user: A User
    :param category_name: A string, the category name
    :return:
    """
    print(get_user_categories(user))
    try:
        return Category.categories.get(name=category_name, user_storage__id=user.id).weight
    except Category.DoesNotExist:
        return 0


def update_user_category_weight(user: User, category_name: str, weight: int):
    """
    This function updates Weight associated with the Category in the
    User's UserStorage that matches a given string with the given weight.
    :param user: A User
    :param category_name: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """
    current_cat = get_user_category(user, category_name)
    if int(weight) == current_cat.weight:
        return
    # Get the user's storage
    user_query = UserStorage.user_storage.get(user=user.id)
    # Remove the old Category
    user_query.categories.remove(current_cat)
    # Get or create category matching name and weight.
    new_cat, created = Category.categories.get_or_create(name=category_name, weight=int(weight))
    # Link the user's storage to the new category.
    if created:
        user_query.categories.add(new_cat)

