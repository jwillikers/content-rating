"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models import Word, Weight, Category, ContentRating, \
    UserStorage, Content, WordCount, CategoryRating
from django.contrib.auth.models import User
from capstoneproject.content_rating.algorithm import text
from django.contrib.auth.models import User
import traceback


def get_categories():
    """
    This function returns all categories that are used to classify offensive content.
    :return: A list of categories stored in the database.
    """
    return Category.categories.all()


def get_category(category):
    """
    This function returns a Category that matches the given category name.
    :param category: A string, the category name
    :return: A Category
    """
    return Category.categories.get(name=category)


def get_user_categories(user: User):
    """
    This function returns a queryset of a User's Categories.
    :param user: A User
    :return: A queryset containing a User's Categories
    """
    print("TODO")  # TODO


def get_user_category(user: User, category: str):
    """
    This function returns a Category model associated with
    the given User and category name.
    :param user: A User
    :param category: A string, the name of the category
    :return: A Category model
    """
    print("TODO")  # TODO


def get_words():
    """
    This function returns all words that are used to classify offensive content.
    :return: A list of all words stored in the system's dictionary of offensive content.
    """
    return Word.words.all()


def get_word(word):
    """
    Gets a Word model that matches the given string.
    :param word: A string, the word name to get.
    :return: A Word
    """
    word_model = None
    try:
        word_model = Word.words.get_word(word=word)
    except TypeError:
        print(traceback.print_exc())
    return word_model


def get_user_word_features(user: User, word: str):
    print("TODO")  # TODO - Need to better define what we will need.


def get_word_weight(user: User, word: str, category: str):
    """
    This function provides the weight associated with a given User, Word, and Category.
    If the user has stored their own word weight, then this value is returned.
    Otherwise, return the default word weight.
    :param user: A User
    :param word: A string, the word name
    :param category: A string, the category name
    :return: An int, the offensiveness weight associated with the given user, word, and category
    """
    print("TODO")  # TODO


def update_user_word_weight(user: User, word: str, category: str, weight: int):
    """
    This function updates the weight associated with the WordFeature of the given
    word and given category to be the given weight.
    :param user: A User
    :param word: A string, the word name
    :param category: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """
    print("TODO")  # TODO


def get_category_words(category):
    """
    This function returns all words that are used to classify offensive content from the given category.
    :param category: The offensive category of words that should be returned.
    :return: A list of words in the given category stored in the system's dictionary of offensive content.
    """
    return Word.words.category(category)


def get_weights():
    """
    This function returns the weight values associated with the possible
    offensiveness levels of the Words.
    :return: a list of the possible offensive weight values
    """
    return WeightField.WEIGHTS


def get_user_category_weight(user: User, category: str):
    """
    This function provides the weight associated with a given User and Category.
    If the user has stored their own category weight, then this value is returned.
    Otherwise return the default category weight.
    :param user: A User
    :param category: A string, the category name
    :return:
    """
    print("TODO")  # TODO


def update_user_category_weight(user: User, category: str, weight: int):
    """
    This function updates Weight associated with the Category in the
    User's UserStorage that matches a given string with the given weight.
    :param user: A User
    :param category: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """
    print("TODO")  # TODO


# user storage should probably not be transparent
# to the rest of the system through here.
def get_user_storage(user: User):
    user_storage_model = None
    try:
        user_storage_model = UserStorage.user_storage.get(id=user.id)
    except TypeError:
        print(traceback.print_exc())
    return user_storage_model[0]


def save_word_count(word: str, count: int):
    """
    This method creates and saves a new WordCount model into the WordCount table.
    :param word: A string, the word to store.
    :param count: An int, the count associated with the word.
    :return: A WordCount model, newly created.
    """
    wc = WordCount.objects.create(
        word=get_word(word),
        count=count)
    print(wc)
    return wc


def save_category_ratings(user: User, category: str, rate):
    """
    This function created and saves a CategoryRatings model into the CategoryRatings table.
    :param user: A User, the user who performed the associated rating.
    :param category: A string, the name of the category.
    :param rate: An int, the rating associated with the category.
    :return: A CategoryRating model, newly created.
    """
    # TODO: Help here - below statement error statement is:
    # 'TypeError: Direct assignment to the forward side of a
    # many-to-many set is prohibited. Use user.set() instead.'
    cr = CategoryRating.objects.get_or_create(
        category=get_category(category).id,
        rating=rate)
    print(cr)
    return cr


def save_rating(rated_content: text.Text, user: User):
    """
    This functions saves the data associated with a user's rating into the database.
    :param rated_content: The data to store.
    :param user: The current User.
    :return: None
    """
    # First create Content
    c = Content.content.get_or_create(
        title=rated_content.title,
        creator=rated_content.creator,
        media=rated_content.content_type)
    # Then create ContentRating
    r = ContentRating.ratings.get_or_create(
        content=c.id,
        rating=rated_content.overall_rating)
    # Next get Word Counts
    for word, count in rated_content.get_word_counts().items():
        wc = save_word_count(word, count)
        #wc = get_or_create(word=word, count=count)
        r.word_counts.add(wc.id)
    # Finally get Category Ratings
    for category, rate in rated_content.category_ratings.items():
        cr = save_category_ratings(user, category, rate)
        r.category_ratings.add(cr)

    r.save()  # Not sure if this is needed.
    print(r)
    # TODO Help Here
    #print(user.userstorage_set.all())
    #user.userstorage_set.add(r)
    us = get_user_storage(user)  # Get the user's storage
    #print(user.userstorage_set.all())
    us.ratings.add(r)  # Add the rating to the user's list of ratings
    #print(us)


def get_user_ratings(user: User):
    """
    This function returns a queryset containing a user's past ratings.
    :param user: A User
    :return: A queryset containing a user's past ratings.
    """
    return UserStorage.user_storage.get(id=user.id).ratings.all()


def get_most_recent_user_rating(user: User):
    """
    This function returns a user's most recent Rating
    :param user: A User
    :return: A queryset containing a user's most recent rating.
    """
    return UserStorage.user_storage.get(id=user.id).ratings.latest('updated')


def get_user_rating_amount(user: User):
    """
    This function returns the amount of Ratings the User has stored
    in their UserStorage. Should be 0-5.
    :param user: A User
    :return: An int, the quantity of Ratings in the User's UserStorage.
    """
    return UserStorage.user_storage.get(id=user.id).ratings.count()


def delete_oldest_user_rating(user: User):
    """
    This function removes the user's oldest Rating stored in their UserStorage.
    This is used when the User has reached their limit of 5 Ratings to be stored.
    :param user: A User
    :return: None
    """
    print("TODO")  # TODO This function will not be needed if we just overwrite the user's oldest Rating.
    # Delete related WordCounts
    # Delete related CategoryRatings


def overwrite_oldest_user_rating(user: User, rating: ContentRating):
    """
    This function overwrites the user's oldest Rating stored in their UserStorage.
    This is used when the User has reached their limit of 5 Ratings to be stored.
    :param user: A User
    :param rating: A Rating model
    :return: None
    """
    print("TODO")  # TODO This function will not be needed if we delete the user's oldest Rating instead.
    # Update/Delete WordCounts of overwritten Rating
    # Update/Delete CategoryRatings of overwritten Rating
