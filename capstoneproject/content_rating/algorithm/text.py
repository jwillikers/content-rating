"""
This file contains the Text class to contain data on the classification and rating of a given text.
"""
from capstoneproject.models import Word
from collections import defaultdict


class Text:
    """
    Class to represent the text to classify and rate.
    """
    offensive_sentences = {}
    sentence_list = []
    total_strongly_offensive_words_dict = defaultdict(int)
    total_weakly_offensive_words_dict = defaultdict(int)
    total_number_of_clean_words = 0
    total_number_of_offensive_words = 0
    overall_rating = 0
    category_ratings = defaultdict(int)

    def __init__(self, text_sentences):
        """
        Initialize a Text object
        :param text_sentences: the sentences contained within the text, a list of Sentence objects.
        """
        self.sentence_list = text_sentences

    def add_strongly_offensive_words(self, offensive_words):
        """
        Use a dictionary of strongly offensive words and their quantities from a single sentence to update the
        text's total count.
        :param offensive_words: A dictionary where the key contains the strongly offensive word and its category
        and the value is the number of times the word occurred within a sentence.
        :return: None
        """
        for key in offensive_words.keys():
            self.total_strongly_offensive_words_dict[key] += offensive_words[key]

    def add_weakly_offensive_words(self, offensive_words):
        """
        Use a dictionary of weakly offensive words and their quantities from a single sentence to update the
        text's total count.
        :param offensive_words: A dictionary where the key contains the weakly offensive word and its category
        and the value is the number of times the word occurred within a sentence.
        :return: None.
        """
        for key in offensive_words.keys():
            self.total_weakly_offensive_words_dict[key] += offensive_words[key]

    def add_offensive_words(self, number_of_offensive_words):
        """
        Update the text's total number of offensive words by adding the given amount.
        :param number_of_offensive_words: The number of offensive words to increase the total number of offensive words
        by.
        :return: None.
        """
        self.total_number_of_offensive_words += number_of_offensive_words

    def add_clean_words(self, number_of_clean_words):
        """
        Update the text's total number of clean words by adding the given amount.
        :param number_of_clean_words: The number of clean words to increase the total number of clean words by.
        :return: None.
        """
        self.total_number_of_clean_words += number_of_clean_words

    def extract_features(self):
        """
        This function extracts the lexical and syntactic features from each sentence.
        :return: None.
        """
        features_path = 'capstoneproject/testing_resources/TotalTextFeatures'
        with open(features_path, 'w') as total_text_feature_file:
            text_features = {}
            features_path = 'capstoneproject/testing_resources/Features'
            with open(features_path, 'w') as feature_file:
                for sent in self.sentence_list:
                    print(sent)
                    featureset = sent.extract_lexical_features()  # Extract the lexical features from each sentence.
                    #print(featureset)
                    feature_file.write(str(featureset) + '\n\n')
                    # sent.extract_syntactic_features()  # Extract the syntactic features from each sentence.
                    print(sent.offensive_categories)
                    text_features['{}:Offensive'.format(sent.sentence_number)] = sent.offensive_categories

                    self.add_strongly_offensive_words(sent.strongly_offensive_words)
                    self.add_weakly_offensive_words(sent.weakly_offensive_words)
                    self.add_offensive_words(sent.number_of_offensive_words)
                    self.add_clean_words(sent.number_of_clean_words)
                text_features['Number of offensive words'] = self.total_number_of_offensive_words
                text_features['Number of clean words'] = self.total_number_of_clean_words
            print(str(text_features))
            total_text_feature_file.write(str(text_features))

    def get_text_features(self):
        """
        This function provides the offensive features of the text.
        :return: None
        """
        print("To do")


    def calculate_offensiveness(self):
        """
        This function calculates the offensiveness of each sentence within the text.
        :return: None.
        """
        print("To do")

    def generate_rating(self):
        """
        This function generates an offensiveness rating using the text's classification data.
        :return: None.
        """
        print("To do")
