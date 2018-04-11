"""
This file contains functions that provide help create the information displayed in the various views.
"""
import os
import capstoneproject.content_rating.algorithm.text as text
from capstoneproject.shared import rater
from capstoneproject import parsing
from django.contrib.auth.models import User
from capstoneproject.helpers import model_helper

from capstoneproject.models import Word, Category, ContentRating, \
    UserStorage, Content, WordCount, CategoryRating, WeightField


def get_file_content(file):
    """
    This function coordinates the collection of text from a file.
    It firsts unloads the file which is originally from the HTML request into a temp file.
    Then it parses the temp file to obtain its text.
    Then it deletes the temp file.
    Lastly it returns the file's text.
    :param file: A file.
    :return: A string, the file's text.
    """
    chunk_uploaded_file(file)  # Transfer file from HTML Request
    file_text = parse_file(file.name)  # Get text from temp file
    os.remove('capstoneproject/tempfile')  # Delete the temp file after use
    return file_text


def chunk_uploaded_file(f):
    """
    This function reads the given file in chunks and writes the file to another file.
    :param f: The file to read.
    :return: None.
    """
    with open('capstoneproject/tempfile', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def parse_file(file_name):
    """
    This function parses the contents of a temporary file based on the type of the file.
    :param file_name: A string, the file name.
    :return: A string, the contents of the file.
    """
    if file_name.endswith('.pdf'):
        file_text = parsing.parse_pdf('capstoneproject/tempfile')
    elif file_name.endswith('.epub'):
        file_text = parsing.parse_epub('capstoneproject/tempfile')
    elif file_name.endswith('docx'):
        file_text = parsing.parse_docx('capstoneproject/tempfile')
    elif file_name.endswith('txt'):
        file_text = parsing.parse_txt('capstoneproject/tempfile')
    else:
        print('ERROR')  # TODO Handle this error
        file_text = ''
    return file_text


def get_weight_dict():
    """
    This function creates a weight dictionary containing
    the numerical and string values associated with the
    possible weights.
    :return: A dictionary
    """
    weight_dict = dict()
    for weight in model_helper.get_weights():
        weight_dict[weight[0]] = weight[1]
    return weight_dict
