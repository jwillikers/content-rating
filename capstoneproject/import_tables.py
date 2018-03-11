#!/usr/bin/env python3
"""Import tables from csv into the database.

This module imports csv files into the
content-rating dictionary tables.

Example:
    comment out the lines in the import_tables
    function for any unused import tables, then
    run.

    $ python3 import_tables.py

Todo:
    * add commandline options for importing tables.
"""
import csv
import os
import django
from django.core.exceptions import ObjectDoesNotExist

# set the django settings and start the django app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# after loading django, import the content-rater models
from capstoneproject.models import Category, Word, Phrase, PhraseSpelling, WordSpelling, WordCategory

# setup simple aliases for the model objects
categories = Category.objects
word_categories = WordCategory.objects
words = Word.objects
phrases = Phrase.objects
word_spellings = WordSpelling.objects
phrase_spellings = PhraseSpelling.objects


def csv_reader(path: str):
    """Open the csv file at the given path.

    Args:
        path (str): path to csv file.

    Returns:
        csv.DictReader: the csv file as dictionary entries.
    """
    f = open(path, 'r')
    print('opened ' + path.rpartition('/')[2])
    reader = csv.DictReader(f)
    print('header fields:')
    for name in reader.fieldnames:
        print('\t' + name)
    return reader


def import_category(path: str):
    """Import category entries into the Category table.

    Args:
        path (str): path to the category csv file.

    Returns:
        None: updates the category table.
    """
    reader = csv_reader(path)

    for category_entry in reader:
        try:
            category = categories.get(category=category_entry['category'])
        except ObjectDoesNotExist:
            category = Category(category=category_entry['category'])

        try:
            category.weight = category_entry['weight']
            category.save()
        except ValueError:
            print('skipping ' + category_entry['category']
                  + '\t\t: weight ' + category_entry['weight'] + ' is not an integer')
            continue

        parents = list()
        for index in [1, 2]:
            parent_name = category_entry['parent' + str(index)]
            if parent_name is not '':
                try:
                    parent = categories.get(category=parent_name)
                except ObjectDoesNotExist:
                    print('skipping ' + category_entry['category']
                          + '\t\t: parent ' + parent_name + ' does not exist')
                    continue
                parents.append(parent)
        category.parent_set.set(parents)

    print('import of csv into category table complete\n')


def import_word(path: str):
    """Import the word entries into the Word table.

    Args:
        path (str): path to the csv of word entries.

    Returns:
        None: updates the Word table.
    """
    reader = csv_reader(path)

    for word_entry in reader:
        word_category_list = list()
        for index in [1, 2, 3]:
            category_name = word_entry['category' + str(index)]
            strong = bool(word_entry['strong' + str(index)])
            weight = word_entry['weight' + str(index)]

            if category_name != '' and strong is not None and weight is not None:
                try:
                    category = categories.get(category=category_name)
                except ObjectDoesNotExist:
                    print('skipping category for ' + word_entry['word'] + '\t\t: category \'' + category_name
                          + '\' does not exist')
                    continue

                try:
                    word_category, _ = word_categories.get_or_create(
                        category_id=category.id,
                        strong=strong,
                        weight=weight
                    )
                except ValueError:
                    print('skipping ' + word_entry['word'] + '\t\t: strong ' + str(strong) + ' is not a boolean')
                    continue

                word_category_list.append(word_category)

        try:
            word = words.get(
                word=word_entry['word']
            )
        except ObjectDoesNotExist:
            word = Word(word=word_entry['word'])

        word.save()

        for word_category in word_category_list:
            word.word_category_set.add(word_category.id)
        word.save()

    print('import of csv into words table complete\n')


def import_phrase(path: str):
    """Import the phrase entries from the csv into the Phrase table.

    Args:
        path: path to the csv holding the Phrase entries.

    Returns:
        None: updates the Phrase table.
    """
    reader = csv_reader(path)

    for phrase_entry in reader:
        try:
            category = categories.get(category=phrase_entry['category'])
        except ObjectDoesNotExist:
            print(
                'skipping ' + phrase_entry['phrase'] + '\t\t: category \'' + phrase_entry[
                    'category'] + '\' does not exist')
            continue

        entry_word_set = list()
        for word_word in [phrase_entry['word1'], phrase_entry['word2'], phrase_entry['word3']]:
            if word_word != '':
                try:
                    entry_word_set.append(words.get(word=word_word))
                except ObjectDoesNotExist:
                    print('skipping ' + phrase_entry['phrase'] + '\t\t: word \'' + word_word + '\' does not exist')
                    continue

            try:
                phrase = phrases.get(phrase=phrase_entry['phrase'])
            except ObjectDoesNotExist:
                phrase = Phrase(phrase=phrase_entry['phrase'])

        phrase.category_id = category.id
        phrase.weight = phrase_entry['weight']
        phrase.save()
        phrase.word_set.clear()
        for word_obj in entry_word_set:
            phrase.word_set.add(word_obj)

    print('import of csv into phrases table complete\n')


def import_phrase_spelling(path: str):
    """Import the phrase spelling entries from the csv into the PhraseSpelling table.

    Args:
        path (str): path to the csv holding the phrase spelling entries.

    Returns:
        None: updates the PhraseSpelling table.
    """
    reader = csv_reader(path)

    for spelling_entry in reader:
        try:
            phrase = phrases.get(phrase=spelling_entry['phrase'])
        except ObjectDoesNotExist:
            print('skipping ' + spelling_entry['spelling']
                  + '\t\t: phrase \'' + spelling_entry['phrase'] + '\' does not exist')
            continue

        phrase_spellings.update_or_create(
            phrase_id=phrase.id,
            spelling=spelling_entry['spelling'],
        )

    print('import of csv into phrases spelling table complete\n')


def import_word_spelling(path: str):
    """Import the word spelling entries from the csv into the WordSpelling table.

    path (str): path to the csv holding the word spelling entries.

    Returns:
        None: imports the spelling table.
    """
    reader = csv_reader(path)

    for spelling_entry in reader:
        try:
            word = words.get(word=spelling_entry['word'])
        except ObjectDoesNotExist:
            print('skipping ' + spelling_entry['spelling'] + '\t\t: word \'' + spelling_entry[
                'word'] + '\' does not exist')
            continue

        word_spellings.update_or_create(
            word_id=word.id,
            spelling=spelling_entry['spelling'],
        )

    print('import of csv into words spelling table complete\n')


def import_tables(root_folder='', category_path='', word_path='', phrase_path='', wordspelling_path='',
                  phrasespelling_path=''):
    """import the tables from the csv files into the dictionary tables.

    Args:
        root_folder (str): path to the folder where the csv's are located.
        category_path (str): path to the category csv file.
        word_path (str): path to the word csv file.
        phrase_path (str): path to the phrase csv file.
        wordspelling_path (str): path to the word spelling csv file.
        phrasespelling_path (str): path to the phrase spelling csv file.

    Returns:
        None: updates the tables in the database.
    """
    if category_path != '':
        import_category(root_folder + category_path)
    if word_path != '':
        import_word(root_folder + word_path)
    if phrase_path != '':
        import_phrase(root_folder + phrase_path)
    if wordspelling_path != '':
        import_word_spelling(root_folder + wordspelling_path)
    if phrasespelling_path != '':
        import_phrase_spelling(root_folder + phrasespelling_path)
    print('\nall imports complete\n')


def main():
    """Import the csv files into the dictionary tables.

    Notes:
        Just comment out the corresponding path names to
        allow for the corresponding tables to be uploaded
        until I get some args stuff setup.

    Returns:
        None: updates the dictionary tables.
    """
    import_tables(
        root_folder='/Users/jwilliams/Downloads/',
        category_path='Category.csv',
        word_path='Word.csv',
        # phrase_path='Phrase.csv',
        # wordspelling_path='WordSpelling.csv',
        # phrasespelling_path='PhraseSpelling.csv'
    )


if __name__ == '__main__':
    """
    call the main method when this module is ran
    """
    main()
