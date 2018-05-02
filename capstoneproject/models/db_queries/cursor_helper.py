"""Utilities for Django Database Cursors"""
from django.db import connection


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    :param cursor:
    :return: the results from the cursor as a dictionary.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row))
            for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    :param cursor: a database cursor
    :return: the results from the cursor as a named tuple.
    """
    from collections import namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
