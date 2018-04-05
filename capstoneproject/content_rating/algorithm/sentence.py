"""
This file contains the Sentence class which contains data on individual sentences within a given text.
"""
import nltk
from capstoneproject.helpers import model_helper


class Sentence:
    """
    The class represents a sentence within the text to be classified and rated.
    """

    def __init__(self, sentence: list, number: int):
        """
        Initialize Sentence object
        :param sentence: A list of (word, part of speech tag) tuples of the sentence represented.
        :param number: The position in the original text that this sentence can be found.
        """
        self.sentence_tokens = nltk.pos_tag(
            sentence)  # List of tuples in the form of (word, part of speech tag) in the sentence.
        self.sentence_number = number  # Location of the sentence within the original text.
        self.offensive_categories = []  # List containing the offensive categories met by this sentence
        self.weakly_offensive_words = dict()  # Dictionary containing weakly offensive word/category pairs
        # and the number of occurrences in the sentence.
        self.strongly_offensive_words = dict()  # Dictionary containing strongly offensive word/category
        # pairs and the number of occurrences in the sentence.
        self.number_of_clean_words = 0  # Number of clean words within the sentence.
        self.number_of_offensive_words = 0  # Number of offensive words within the sentence.
        self.initialize_word_dictionaries()

    def __str__(self):
        """
        Overwrite to string function
        :return: A string giving information about the sentence.
        """
        string = 'Sent {}: {}\n'.format(self.sentence_number, self.sentence_tokens)
        string += '  Total Clean Words: {}'.format(self.number_of_clean_words)
        string += '  Total Offensive Words: {}\n'.format(self.number_of_offensive_words)
        string += '  Strongly Offensive Words: {}\n'.format(self.strongly_offensive_words)
        string += '  Weakly Offensive Words: {}\n'.format(self.weakly_offensive_words)
        string += '  Offensive Categories: {}\n'.format(self.offensive_categories)
        return string

    def initialize_word_dictionaries(self):
        """
        Initialize the weakly_offensive_words dictionary and strongly_offensive_words dictionary to have the keys
        be the categories name and each value is another dictionary that will store the word and word counts in the
        appropriate category.
        :return: None.
        """
        for category in model_helper.get_categories():
            self.weakly_offensive_words['{}'.format(category.name)] = dict()
            self.strongly_offensive_words['{}'.format(category.name)] = dict()

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
        try:
            self.strongly_offensive_words[category][word] += 1
        except KeyError:
            self.strongly_offensive_words[category][word] = 1
        if category not in self.offensive_categories:
            self.offensive_categories.append(category)

    def add_weakly_offensive_word(self, word: str, category: str):
        """
        Add an offensive word to the sentence's dictionary of weakly offensive words.
        :param word: The weakly offensive word.
        :param category: The category in which the word is weakly offensive.
        :return: None
        """
        try:
            self.weakly_offensive_words[category][word] += 1
        except KeyError:
            self.weakly_offensive_words[category][word] = 1

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
        for word, POS_tag in self.sentence_tokens:
            off_word = model_helper.get_word(word=word)
            if not off_word:  # Not an offensive word
                # Update the total number of clean words in the sentence.
                self.number_of_clean_words += 1
            else:
                # Update the total number of strongly offensive words in the sentence.
                self.number_of_offensive_words += 1
                for word_cat in off_word.get_word_features():  # each category.
                    if word_cat['strength']:  # Check if the word is strongly or weakly offensive
                        self.add_strongly_offensive_word(word=word, category=word_cat['category'])
                    else:
                        self.add_weakly_offensive_word(word=word, category=word_cat['category'])

    def extract_syntactic_features(self):
        """
        This function extracts the syntactic features from the sentence to determine if it is offensive given data on
        the sentence's weakly offensive words.
        :return: None.
        """
        print("To Do")
