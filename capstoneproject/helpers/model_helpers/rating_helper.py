"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.models.content import Content
from capstoneproject.models.models.word_count import WordCount
from capstoneproject.models.models.category_rating import CategoryRating
from django.contrib.auth.models import User
from capstoneproject.helpers.model_helpers import category_helper, word_helper


def save_word_count(word_name: str, count_value: int):
    """
    This method creates and saves a new WordCount model into the WordCount table.
    :param word_name: A string, the word to store.
    :param count_value: An int, the count associated with the word.
    :return: A WordCount model, newly created.
    """
    wc, _ = WordCount.word_counts.get_or_create(
        word=word_helper.get_word(word_name=word_name),
        count=count_value)
    return wc


def save_category_ratings(category_name: str, rate_value):
    """
    This function created and saves a CategoryRatings model into the CategoryRatings table.
    :param category_name: A string, the name of the category.
    :param rate_value: An int, the rating associated with the category.
    :return: A CategoryRating model, newly created.
    """
    category_model = category_helper.get_default_category(category_name=category_name)
    cr, created = CategoryRating.category_ratings.get_or_create(
        category=category_model,
        rating=rate_value)
    return cr


def clear_ratings_databases():
    """
    This function clears the Content, ContentRating,
    CategoryRating, and WordCount tables.
    :return: None.
    """
    Content.content.all().delete()
    ContentRating.content_ratings.all().delete()
    CategoryRating.category_ratings.all().delete()
    WordCount.word_counts.all().delete()


def update_user_ratings(rated_content, user: User):
    """
    This function updates the user's saved ratings by
    adding the given rating to the user's storage.
    If the user already has 5 or more past ratings saved,
    then the oldest updated reviews are removed until
    the user can save their newest review.
    :param rated_content: The data to store
    :param user: A User, the current User
    :return: None
    """
    while get_user_rating_amount(user) >= 5:  # Check if the user has reached their limit.
        print("\nDELETE\n")
        delete_oldest_user_rating(user)  # Remove oldest ratings if so.
    save_rating(rated_content, user)  # Save the new rating


def save_rating(rated_content, user: User):
    """
    This functions saves the data associated with a user's rating into the database.
    :param rated_content: The data to store.
    :param user: A User, the current User.
    :return: None
    """
    # First create Content
    c, _ = Content.content.get_or_create(
        title=rated_content.title,
        creator=rated_content.creator,
        media=rated_content.content_type)
    print("\n\nCONTENT")
    print(c)
    # Then create ContentRating
    r = ContentRating.content_ratings.create(
        content=c,
        rating=rated_content.overall_rating
    )
    print("\n\nCONTENT RATING")
    print(r)
    # Next get Word Counts
    for word, count in rated_content.get_word_counts().items():
        wc = save_word_count(word_name=word, count_value=count)
        r.word_counts.add(wc)
    # Finally get Category Ratings
    for category_name, rate_value in rated_content.category_ratings.items():
        cr = save_category_ratings(category_name=category_name, rate_value=rate_value)
        r.category_ratings.add(cr.id)

    r.save()
    UserStorage.user_storage.get(
        user=user.id).ratings.add(r)
    print("\n\nUSER RATINGS")
    print(UserStorage.user_storage.get(user=user.id).ratings.all())


def get_user_ratings(user: User):
    """
    This function returns a queryset containing a user's past ratings.
    :param user: A User
    :return: A queryset containing a user's past ratings.
    """
    return ContentRating.content_ratings.filter(user_storage__id=user.id).order_by('-updated')


def get_user_rating_at_position(user: User, pos: int):
    """
    This function returns a user's rating at a given index position from a list
    ordered so the most recently updated rating is first.

    :param user: A User
    :param pos: An int, the position in the user's past ratings that should be returned.
    :return: A queryset containing a user's most recent rating.
    """
    try:
        print("\n\nOrdered User Ratings")
        print(ContentRating.content_ratings.filter(
            user_storage__id=user.id).order_by('-updated'))
        return ContentRating.content_ratings.filter(
            user_storage__id=user.id).order_by('-updated')[pos]
    except IndexError:
        return None


def get_user_rating_amount(user: User):
    """
    This function returns the amount of Ratings the User has stored
    in their UserStorage. Should be 0-5.
    :param user: A User
    :return: An int, the quantity of Ratings in the User's UserStorage.
    """
    print('\n\nUSER AMOUNT: ' + str(ContentRating.content_ratings.filter(
        user_storage__id=user.id).count()))
    return ContentRating.content_ratings.filter(
        user_storage__id=user.id).count()


def delete_oldest_user_rating(user: User):
    """
    This function removes the user's oldest Rating stored in their UserStorage.
    This is used when the User has reached their limit of 5 Ratings to be stored.
    :param user: A User
    :return: None
    """
    oldest_rating = ContentRating.content_ratings.filter(
        user_storage__id=user.id).earliest('updated')
    oldest_rating.delete()
