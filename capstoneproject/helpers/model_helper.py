"""
This file contains functions used to provide data from the database.
"""
from capstoneproject.models import Word, Category, ContentRating, \
    UserStorage, Content, WordCount, CategoryRating, WeightField
#from capstoneproject.content_rating.algorithm import text
from django.contrib.auth.models import User
import traceback


def get_categories():
    """
    This function returns all categories that are used to classify offensive content.
    :return: A list of categories stored in the database.
    """
    return Category.categories.filter(default=True)


def get_category(category_name):
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
    return Category.categories.filter(user_storage__id=user.id, default=True)


def get_user_category(user: User, category_name: str):
    """
    This function returns a Category model associated with
    the given User and category name.
    :param user: A User
    :param category_name: A string, the name of the category
    :return: A Category model
    """
    return Category.categories.get(name=category_name, user_storage__id=user.id, default=True)


def get_words():
    """
    This function returns all words that are used to classify offensive content.
    :return: A list of all words stored in the system's dictionary of offensive content.
    """
    return Word.words.all()

def get_word(word_name: str):
    """
    Gets a Word model that matches the given string.
    :param word_name: A string, the word name to get.
    :return: A Word
    """
    word_model = None
    try:
        word_model = Word.words.get_word(word=word_name)
    except TypeError:
        print(traceback.print_exc())
    return word_model


def get_user_word_features(user: User, word: str):
    return Word.words.get(name=word).word_features.filter(user_storage__id=user.id)


def get_word_weight(user: User, word_name: str, category_name: str):
    """
    This function provides the weight associated with a given User, Word, and Category.
    If the user has stored their own word weight, then this value is returned.
    Otherwise, return the default word weight.
    :param user: A User
    :param word_name: A string, the word name
    :param category_name: A string, the category name
    :return: An int, the offensiveness weight associated with the given user, word, and category
    """
    return Word.words.get(name=word_name).word_features.get(
        user_storage__id=user.id, category__name=category_name).weight


def update_user_word_weight(user: User, word_name: str, category_name: str, weight: int):
    """
    This function updates the weight associated with the WordFeature of the given
    word and given category to be the given weight.
    :param user: A User
    :param word_name: A string, the word name
    :param category_name: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """
    return Word.words.get(name=word_name).word_features.get(
        user_storage__id=user.id, category__name=category_name).update(weight=weight)


def get_category_words(category_name):
    """
    This function returns all words that are used to classify offensive content from the given category.
    :param category_name: The offensive category of words that should be returned.
    :return: A list of words in the given category stored in the system's dictionary of offensive content.
    """
    return Word.words.category(category_name)


def get_weights():
    """
    This function returns the weight values associated with the possible
    offensiveness levels of the Words.
    :return: a list of the possible offensive weight values
    """
    return WeightField.WEIGHTS


def get_user_category_weight(user: User, category_name: str):
    """
    This function provides the weight associated with a given User and Category.
    If the user has stored their own category weight, then this value is returned.
    Otherwise return the default category weight.
    :param user: A User
    :param category_name: A string, the category name
    :return:
    """
    return Category.categories.get(name=category_name, user_storage__id=user.id).weight


def update_user_category_weight(user: User, category_name: str, weight: int):
    """
    This function updates Weight associated with the Category in the
    User's UserStorage that matches a given string with the given weight.
    :param user: A User
    :param category_name: A string, the category name
    :param weight: An int, the new Weight value (0-3)
    :return: None
    """
    return Category.categories.get(
        name=category_name, user_storage__id=user.id).update(weight=weight)


# user storage should probably not be transparent
# to the rest of the system through here.
def get_user_storage(user: User):
    user_storage_model = None
    try:
        user_storage_model = UserStorage.user_storage.get(id=user.id)
    except TypeError:
        print(traceback.print_exc())
    return user_storage_model[0]


def save_word_count(word_name: str, count_value: int):
    """
    This method creates and saves a new WordCount model into the WordCount table.
    :param word_name: A string, the word to store.
    :param count_value: An int, the count associated with the word.
    :return: A WordCount model, newly created.
    """
    wc, _ = WordCount.objects.get_or_create(
        word=get_word(word_name=word_name),
        count=count_value)
    return wc


def save_category_ratings(category_name: str, rate_value):
    """
    This function created and saves a CategoryRatings model into the CategoryRatings table.
    :param category_name: A string, the name of the category.
    :param rate_value: An int, the rating associated with the category.
    :return: A CategoryRating model, newly created.
    """
    category_model = get_category(category_name=category_name)
    cr, created = CategoryRating.objects.get_or_create(
        category=category_model,
        rating=rate_value)
    return cr


def clear_databases():
    """
    This function clears the Content, ContentRating,
    CategoryRating, and WordCount tables.
    :return: None.
    """
    Content.content.all().delete()
    ContentRating.content_ratings.all().delete()
    CategoryRating.objects.all().delete()
    WordCount.objects.all().delete()


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
    # Then create ContentRating
    r, _ = ContentRating.content_ratings.get_or_create(
        content=c,
        rating=rated_content.overall_rating)
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


def get_user_ratings(user: User):
    """
    This function returns a queryset containing a user's past ratings.
    :param user: A User
    :return: A queryset containing a user's past ratings.
    """
    return ContentRating.content_ratings.filter(user_storage__id=user.id)


def get_user_rating_at_position(user: User, pos: int):
    """
    This function returns a user's rating at a given index position from a list
    ordered so the most recently updated rating is first.

    :param user: A User
    :param pos: An int, the position in the user's past ratings that should be returned.
    :return: A queryset containing a user's most recent rating.
    """
    try:
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
    #word_counts = oldest_rating.word_counts.all()
    #for wc in word_counts:
    #    WordCount.delete(wc)
    #category_rating = oldest_rating.category_ratings.all()
    #for cr in category_rating:
    #    CategoryRating.delete(cr)
    # oldest_rating.word_counts.delete() #
    # oldest_rating.category_ratings.delete()
    oldest_rating.delete()
