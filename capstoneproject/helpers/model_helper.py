"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.fields.weight_field import WeightField
from django.contrib.auth.models import User
import traceback


def get_weights():
    """
    This function returns the weight values associated with the possible
    offensiveness levels of the Words.
    :return: a list of the possible offensive weight values
    """
    return WeightField.WEIGHTS


# user storage should probably not be transparent
# to the rest of the system through here.
def get_user_storage(user: User):
    """
    This function returns the UserStorage model associated with the given User.
    :param user: A User
    :return: A UserStorage model or None
    """
    user_storage_model = None
    try:
        user_storage_model = UserStorage.user_storage.get(id=user.id)
    except TypeError:
        print(traceback.print_exc())
    return user_storage_model[0]
