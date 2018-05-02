"""Raw SQL for retrieving the Words and their Features belonging to a User."""
from django.db import connection
from capstoneproject.models.db_queries.cursor_helper import dictfetchall


def words_and_features(
        user_id=None,
        category_id=None,
        strength=None):
    """
    Retrieve Words and their Features belonging to Users.
    :param user_id: User that owns the Words and Features.
    :param category_id: WordFeatures belonging to a specific Category.
    :param strength: Strength of the WordFeature to retrieve
    :return: a dictionary of objects representing the WordFeature.
    """
    query_string = '''
SELECT
    w.id AS word_id,
    w.name AS word,
    f.category_id,
    f.strength,
    f.weight
'''
    user_from_query_string = '''
FROM capstoneproject_userstorage AS u
INNER JOIN capstoneproject_userstorage_words AS uw
    ON u.id = uw.userstorage_id
INNER JOIN capstoneproject_word AS w
    ON uw.word_id = w.id
INNER JOIN capstoneproject_userstorage_word_features AS uf
    ON u.id = uf.userstorage_id
INNER JOIN capstoneproject_wordfeature AS f
    ON uf.wordfeature_id = f.id
'''
    all_from_query_string = '''
FROM capstoneproject_word AS w
INNER JOIN capstoneproject_word_word_features AS wf
    ON wf.word_id = w.id
INNER JOIN capstoneproject_wordfeature AS f
    ON wf.wordfeature_id = f.id
'''
    first = True
    query_variables = list()

    if user_id is not None:
        query_string += user_from_query_string
    else:
        query_string += all_from_query_string

    if user_id is not None:
        query_variables.append(user_id)
        if first:
            first = False
            query_string += '\nWHERE'
        else:
            query_string += '\nAND'
        query_string += ' uw.userstorage_id = %s'
    if category_id is not None:
        query_variables.append(category_id)
        if first:
            first = False
            query_string += '\nWHERE'
        else:
            query_string += '\nAND'
        query_string += ' f.category_id = %s'
    if strength is not None:
        query_variables.append(strength)
        if first:
            first = False
            query_string += '\nWHERE'
        else:
            query_string += '\nAND'
        query_string += ' f.strength = %s'

    with connection.cursor() as cursor:
        cursor.execute(query_string, query_variables)
        rows = dictfetchall(cursor)
    return rows
