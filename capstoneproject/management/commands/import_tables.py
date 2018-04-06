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
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import capstoneproject.models as models
from capstoneproject.models import Category
from capstoneproject.models import Word
from capstoneproject.models import WordFeature

# setup simple aliases for the model objects
categories = Category.categories
word_features = WordFeature.word_features
words = Word.words


class Command(BaseCommand):
    def csv_reader(self, path: str):
        """
        Open the csv file at the given path.
        :param path: A string of the path to the csv file.
        :return: a csv.DictReader, a csv file as dictionary entries.
        """
        f = open(path, 'r')
        self.stdout.write('opened ' + path.rpartition('/')[2])
        reader = csv.DictReader(f)
        self.stdout.write('header fields:')
        for name in reader.fieldnames:
            self.stdout.write('\t' + name)
        return reader

    def import_category(self, path: str):
        """
        Import category entries into the Category table.
        :param path: a string, the path to the category csv file.
        :return: None
        """
        reader = self.csv_reader(path)

        for category_entry in reader:
            try:
                category = categories.get(name=category_entry['category'])
            except ObjectDoesNotExist:
                category = Category(
                    name=category_entry['category'], default=True)

            try:
                category.weight = category_entry['weight']
                category.save()
            except ValueError:
                self.stdout.write(
                    '''skipping {} \t\t: weight {} is not an integer'''.format(
                        categor_entry['category'], category_entry['weight']))
                continue
        self.stdout.write('import of csv into category table complete\n')

    def import_word(self, path: str):
        """
        Import the word entries into the Word table.
        :param path: a string, the path to the csv of word entries.
        :return: None
        """
        reader = self.csv_reader(path)

        for word_entry in reader:
            word_feature_list = list()
            for index in [1, 2, 3]:
                category_name = word_entry['category' + str(index)]
                strength = bool(word_entry['strength' + str(index)])
                weight = word_entry['weight' + str(index)]

                if category_name != '' \
                    and strength is not None \
                        and weight is not None:
                    try:
                        category = categories.get(name=category_name)
                    except ObjectDoesNotExist:
                        self.stdout.write(
                            '''skipping category for {}\t\t: category {} does
                            not exist'''.format(
                                word_entry['word'], category_name))
                        continue

                    try:
                        word_feature, _ = word_features.get_or_create(
                            default=True,
                            category_id=category.id,
                            strength=strength,
                            weight=weight)
                    except ValueError:
                        self.stdout.write(
                            '''skipping {}:\t\tstrength {} is not a boolean
                            '''.format(word_entry['word'], str(strength)))
                        continue

                    word_feature_list.append(word_feature)

            try:
                word = words.get(name=word_entry['word'])
            except ObjectDoesNotExist:
                word = Word(default=True, name=word_entry['word'])
            word.save()

            for feature in word_feature_list:
                word.word_features.add(feature.id)
            word.save()

        self.stdout.write('import of csv into words table complete\n')

    def import_tables(self, root_folder='', category_path='', word_path=''):
        """
        Import the tables from the csv files into the dictionary tables.
        :param root_folder: a string, the path to the folder where the csv's are located.
        :param category_path: a string, the path to the category csv file.
        :param word_path: a string, the path to the word csv file.
        :return: None
        """
        if category_path != '':
            self.import_category(root_folder + category_path)
        if word_path != '':
            self.import_word(root_folder + word_path)
        self.stdout.write('\nall imports complete\n')

    def handle(self, *args, **options):
        """
        Imports tables from the root folder, category path, and word path.
        :param args:
        :param options:
        :return: None.
        """
        self.import_tables(root_folder='/Users/jwilliams/Downloads/',
                           category_path='Category.csv',
                           word_path='Word.csv')
