from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row))
            for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    from collections import namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def words_and_features(user_id=None,
                       category_id=None, strength=None):
    """All Words and their Features belonging to Users."""
    query_string = '''
SELECT
    w.id AS word_id,
    w.name AS word,
    f.category_id,
    f.strength,
    f.weight

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
    first = True
    query_variables = list()

    if user_id:
        query_variables.append(user_id)
        if first:
            query_string += '\nWHERE'
            first = False
        else:
            query_string += '\nAND'
        query_string += ' uw.userstorage_id = %s'
    if category_id:
        query_variables.append(category_id)
        if first:
            query_string += '\nWHERE'
            first = False
        else:
            query_string += '\nAND'
        query_string += ' f.category_id = %s'
    if strength:
        query_variables.append(strength)
        if first:
            query_string += '\nWHERE'
            first = False
        else:
            query_string += '\nAND'
        query_string += ' f.strength = %s'

    with connection.cursor() as cursor:
        cursor.execute(query_string, query_variables)
        rows = dictfetchall(cursor)
    return rows
