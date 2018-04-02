"""
This file contains the Sentence class which contains data on individual sentences within a given text.
"""
import nltk
from capstoneproject.models import Category, Word
from collections import defaultdict


class Sentence:
    """
    The class represents a sentence within the text to be classified and rated.
    """
    '''
    sentence_number = 0  # Location of the sentence within the original text.
    number_of_clean_words = 0      # Number of clean words within the sentence.
    number_of_offensive_words = 0  # Number of offensive words within the sentence.
    sentence_tokens = []  # List of tuples in the form of (word, part of speech tag) in the sentence.
    strongly_offensive_words = defaultdict(int)  # Dictionary containing strongly offensive word/category pairs and
    # the number of occurrences in the sentence.
    weakly_offensive_words = defaultdict(int)    # Dictionary containing weakly offensive word/category pairs and the
    # number of occurrences in the sentence.
    offensive_categories = []                    # List containing the offensive categories met by this sentence
    '''

    def __init__(self, sentence: list, number: int):
        """
        Initialize Sentence object
        :param sentence: A list of (word, part of speech tag) tuples of the sentence represented.
        :param number: The position in the original text that this sentence can be found.
        """
        self.sentence_tokens = nltk.pos_tag(sentence)
        self.sentence_number = number
        self.offensive_categories = []
        self.weakly_offensive_words = defaultdict(int)
        self.strongly_offensive_words = defaultdict(int)
        self.number_of_clean_words = 0
        self.number_of_offensive_words = 0

    def __str__(self):
        """
        To string function
        :return: A string giving information about the sentence.
        """
        return 'Sent {}:{}'.format(self.sentence_number, self.sentence_tokens)

    def set_clean_words(self, number: int):
        """
        Set the sentence's number of non-offensive words to the given amount.
        :param number: The number of non-offensive words in the sentence.
        :return: None
        """
        self.number_of_clean_words = number

    def set_offensive_words(self, number: int):
        """
        Set the sentence's number of offensive words of any category to the given amount.
        :param number: The number of offensive words in the sentence.
        :return: None
        """
        self.number_of_offensive_words = number

    def set_strongly_offensive_words(self, word_dict):
        """
        Set the sentence's dictionary of strongly offensive words to the given dictionary.
        :param word_dict: The dictionary to set as the sentence's dictionary of strongly offensive words.
        :return: None
        """
        self.strongly_offensive_words = word_dict

    def set_weakly_offensive_words(self, word_dict):
        """
        Set the sentence's dictionary of weakly offensive words to the given dictionary.
        :param word_dict: The dictionary to set as the sentence's dictionary of weakly offensive words.
        :return: None
        """
        self.weakly_offensive_words = word_dict

    def add_strongly_offensive_word(self, word: str, category: str):
        """
        Add an offensive word to the sentence's dictionary of strongly offensive words.
        :param word: The strongly offensive word.
        :param category: The category in which the word is strongly offensive.
        :return: None
        """
        self.strongly_offensive_words['{}:{}'.format(word, category)] += 1
        if category not in self.offensive_categories:
            self.offensive_categories.append(category)

    def add_weakly_offensive_word(self, word: str, category: str):
        """
        Add an offensive word to the sentence's dictionary of weakly offensive words.
        :param word: The weakly offensive word.
        :param category: The category in which the word is weakly offensive.
        :return: None
        """
        self.weakly_offensive_words['{}:{}'.format(word, category)] += 1

    def get_sentence_features(self):
        """
        This method returns a dictionary of sentence features to determine the sentence's offensiveness.
        :return: a dictionary of features to determine the sentence's offensiveness.
        """
        # Get number of clean words and offensive words
        features = {'sent_clean_words': self.number_of_clean_words,
                    'sent_offensive_words': self.number_of_offensive_words}
        # Get categories of offensive words
        for word in self.strongly_offensive_words.keys():
            features[word] = self.strongly_offensive_words[word]
        for word in self.weakly_offensive_words.keys():
            features[word] = self.weakly_offensive_words[word]
        for category in self.offensive_categories:
            features['offensive:{}'.format(category)] = True
        return features

    def extract_lexical_features(self):
        """
        This function derives lexical features from the tokenized sentence.
        :return: a set of lexical features.
        """
        non_offensive_words = 0
        offensive_words = 0

        for word, POS_tag in self.sentence_tokens:
            try:
                query = Word.objects.get(word=word)  # Throws a DoesNotExist exception if the word is not offensive.
                offensive_words += 1

                for word_cat in query.word_category_set.all():  # Check if the word is strongly or weakly offensive for
                    # each category.
                    if word_cat.strong:
                        self.add_strongly_offensive_word(word=word, category=word_cat.category.category)
                    else:
                        self.add_weakly_offensive_word(word=word, category=word_cat.category.category)
            except Word.DoesNotExist:
                non_offensive_words += 1
        # Update the total number of clean and offensive words in the sentence.
        self.set_clean_words(non_offensive_words)
        self.set_offensive_words(offensive_words)

        return self.get_sentence_features()

    def extract_syntactic_features(self):
        """
        This function extracts the syntactic features from the sentence to determine if it is offensive given data on
        the sentence's weakly offensive words.
        :return: None.
        """
        print("To Do")
