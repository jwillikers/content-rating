"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models import Word, Weight, Category, Rating, \
    UserStorage, Content, WordCount, CategoryRating, User
from capstoneproject.content_rating.algorithm import text
import traceback


def get_categories():
    """
    This function returns all categories that are used to classify offensive content.
    :return: A list of categories stored in the database.
    """
    return Category.categories.all()


def get_category(category):
    return Category.categories.get(name=category)


def get_words():
    """
    This function returns all words that are used to classify offensive content.
    :return: A list of all words stored in the system's dictionary of offensive content.
    """
    return Word.words.all()


def get_word(word):
    word_model = None
    try:
        word_model = Word.words.get_word(word=word)
    except TypeError:
        print(traceback.print_exc())
    return word_model


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
    return Weight.WEIGHTS


def get_user_storage(user: User):
    user_storage_model = None
    try:
        user_storage_model = UserStorage.user_storage.get_or_create(user=user)
    except TypeError:
        print(traceback.print_exc())
    return user_storage_model[0]


def save_word_count(word: str, count: int):
    wc = WordCount.objects.create(word=get_word(word), count=count)
    print(wc)
    return wc


def save_category_ratings(user: User, category: str, rate):
    cr = CategoryRating.objects.create(user=user, category=get_category(category), rating=rate)
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
    c = Content.content.create(title=rated_content.title,
                creator=rated_content.creator,
                media=rated_content.content_type)
    # Then create Rating
    r = Rating.ratings.create(content=c, rating=rated_content.overall_rating)
    # Next get Word Counts
    for word, count in rated_content.get_word_counts().items():
        wc = save_word_count(word, count)
        r.word_counts.add(wc)
    # Finally get Category Ratings
    for category, rate in rated_content.category_ratings.items():
        cr = save_category_ratings(user, category, rate)
        r.category_ratings.add(cr)

    r.save()  # Not sure if this is needed.
    print(r)
    #print(user.userstorage_set.all())
    #user.userstorage_set.add(r)
    us = get_user_storage(user)  # Get the user's storage
    #print(user.userstorage_set.all())
    us.ratings.add(r)  # Add the rating to the user's list of ratings
    #print(us)


