"""Cursor-based retrieval of Categories per User"""
from django.db import connection
from capstoneproject.models.db_queries.cursor_helper import dictfetchall


def categories(user_id=None, default=False):
    """
    Return the categories for the given user.
    :param user_id: the id of the user that owns the Categories.
    :param default: whether or not to include the default Categories.
    :return: a list of Category object 3-tuples \
    containing id, name, and weight.
    """
    query_string = '''
SELECT
    c.id,
    c.name,
    c.weight

FROM capstoneproject_category AS c

'''
    first = True
    query_variables = list()

    if user_id:
        query_variables.append(user_id)
        if first:
            first = False
            query_string += '''
INNER JOIN capstoneproject_userstorage_categories AS uc
    ON uc.category_id = c.id

WHERE uc.userstorage_id = %s
'''
    if default:
        query_variables.append(default)
        if first:
            first = False
            query_string += '\nWHERE'
        else:
            query_string += '\nAND'
        query_string += """ c."default" = %s"""

    with connection.cursor() as cursor:
        cursor.execute(query_string, query_variables)
        rows = dictfetchall(cursor)
    return rows
