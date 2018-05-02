"""
This file contains the Sentence class which contains data on individual sentences within a given text.
"""
import nltk
from capstoneproject.helpers.model_helpers import category_helper, word_helper


class Sentence:
    """
    The class represents a sentence within the text to be classified and rated.
    """

    def __init__(self, sentence: list, number: int, user):
        """
        Initialize Sentence object
        :param sentence: A list of (word, part of speech tag) tuples of the sentence represented.
        :param number: The position in the original text that this sentence can be found.
        :param user: a User
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
        self.number_of_weak_words = 0  # Number of weakly offensive words within the sentence.
        self.initialize_word_dictionaries(user)

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

    def initialize_word_dictionaries(self, user):
        """
        Initialize the weakly_offensive_words dictionary and strongly_offensive_words
        dictionary to have the keys be the categories name and each value is another
        dictionary that will store the word and word counts in the appropriate category.
        :param user: a User
        :return: None.
        """
        for category in category_helper.get_user_categories(user):
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

    def extract_lexical_features(self, user):
        """
        This function derives lexical features from the tokenized sentence.
        :param user: a User
        :return: a set of lexical features.
        """
        for word, POS_tag in self.sentence_tokens:
            off_word = word_helper.get_word(word_name=word)
            # print("OFFWORD")
            # print(off_word)
            if not off_word:  # Not an offensive word
                # Update the total number of clean words in the sentence.
                self.number_of_clean_words += 1
            else:
                # print("WORD FEATURES")
                # print(off_word.get_word_features())
                strong = False
                for word_cat in off_word.get_word_features():  # each category.
                    if word_cat['strength']:  # Check if the word is strongly or weakly offensive
                        self.add_strongly_offensive_word(word=word, category=word_cat['category'])
                        strong = True
                    else:
                        print("WEAK: " + str(off_word))
                        self.add_weakly_offensive_word(word=word, category=word_cat['category'])
                if strong:
                    # Update the total number of strongly offensive words in the sentence.
                    self.number_of_offensive_words += 1
                else:
                    self.number_of_weak_words += 1
        self.extract_syntactic_features(user)

    def extract_syntactic_features(self, user):
        """
        This function extracts the syntactic features from the sentence to
        determine if it is offensive given data on the sentence's weakly offensive words.
        :param user: a User
        :return: None.
        """
        if len(self.sentence_tokens) != 0:
            weak_ratio = self.number_of_weak_words / len(self.sentence_tokens)
            print("WEAK RATIO: " + str(weak_ratio))
            if weak_ratio >= 0.20 or (self.number_of_offensive_words > 1 and self.number_of_weak_words > 0):
                for cat, word_dic in self.weakly_offensive_words.items():
                    for word, count in word_dic.items():
                        self.add_strongly_offensive_word(word=word, category=cat)
                print("NUM OFF WORDS: " + str(self.number_of_offensive_words))
                self.number_of_offensive_words += self.weakly_offensive_words
                self._reset_weak_resources(user)
                print("NUM OFF WORDS: " + str(self.number_of_offensive_words))

    def _reset_weak_resources(self, user):
        """
        This function resets the weakly_offensive_words dictionary
        and the number of weakly offensive words.
        :param user: A User
        :return: None
        """
        for category in category_helper.get_user_categories(user):
            self.weakly_offensive_words['{}'.format(category.name)] = dict()
        self.number_of_weak_words = 0
