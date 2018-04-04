"""
This file contains the Text class to contain data on the classification and rating of a given text.
"""
from capstoneproject import model_helper


class Text:
    """
    Class to represent the text to classify and rate.
    """

    def __init__(self, text_sentences):
        """
        Initialize a Text object
        :param text_sentences: the sentences contained within the text, a list of Sentence objects.
        """
        self.offensive_sentences = dict()
        self.sentence_list = text_sentences
        self.total_strongly_offensive_words_dict = dict()
        self.total_weakly_offensive_words_dict = dict()
        self.total_number_of_clean_words = 0
        self.total_number_of_offensive_words = 0
        self.overall_rating = 1
        self.category_ratings = dict()
        self.category_word_counts = dict()
        self.initialize_ratings()

    def __str__(self):
        """
        Overwrite to string function
        :return: A string giving information about the sentence.
        """
        string = 'Text:\n'
        string += '  Total Clean Words: {}'.format(self.total_number_of_clean_words)
        string += '  Total Offensive Words: {}\n'.format(self.total_number_of_offensive_words)
        string += '  Offensive Sentences: {}\n'.format(self.offensive_sentences)
        string += '  Total Strongly Offensive Words Dictionary: {}\n'.format(self.total_strongly_offensive_words_dict)
        string += '  Total Weakly Offensive Words Dictionary: {}\n'.format(self.total_weakly_offensive_words_dict)
        string += '  Category Word Counts: {}\n'.format(self.category_word_counts)
        string += '  Category Ratings: {}\n'.format(self.category_ratings)
        string += '  Overall Rating: {}'.format(self.overall_rating)
        return string

    def initialize_ratings(self):
        """
        Initialize the category_ratings, category_word_counts, total_strongly_offensive_words, and
        total_weakly_offensive_words dictionaries to have the keys be the names of all categories, and each value
        is another dictionary.
        :return: None.
        """
        for category in model_helper.get_categories():
            self.category_ratings['{}'.format(category.name)] = 1
            self.category_word_counts['{}'.format(category.name)] = dict()
            self.total_strongly_offensive_words_dict['{}'.format(category.name)] = dict()
            self.total_weakly_offensive_words_dict['{}'.format(category.name)] = dict()
        self.overall_rating = 0

    def add_strongly_offensive_words(self, offensive_words):
        """
        Use a dictionary of strongly offensive words and their quantities from a single sentence to update the
        text's total count.
        :param offensive_words: A dictionary where the key contains the strongly offensive word and its category
        and the value is the number of times the word occurred within a sentence.
        :return: None
        """
        for category, value in offensive_words.items():
            for word, word_count in offensive_words[category].items():
                try:
                    self.category_word_counts[category][word] += word_count
                except KeyError:
                    self.category_word_counts[category][word] = word_count

    def add_weakly_offensive_words(self, offensive_words):
        """
        Use a dictionary of weakly offensive words and their quantities from a single sentence to update the
        text's total count.
        :param offensive_words: A dictionary where the key contains the weakly offensive word and its category
        and the value is the number of times the word occurred within a sentence.
        :return: None.
        """
        for category, value in offensive_words.items():
            for word, word_count in offensive_words[category].items():
                try:
                    self.category_word_counts[category][word] += word_count
                except KeyError:
                    self.category_word_counts[category][word] = word_count

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
                    sent.extract_lexical_features()  # Extract the lexical features from each sentence.
                    print(sent)
                    feature_file.write(str(sent) + '\n\n')
                    # sent.extract_syntactic_features()  # Extract the syntactic features from each sentence.
                    text_features['{}:Offensive'.format(sent.sentence_number)] = sent.offensive_categories

                    self.add_strongly_offensive_words(sent.strongly_offensive_words)
                    self.add_weakly_offensive_words(sent.weakly_offensive_words)
                    self.add_offensive_words(sent.number_of_offensive_words)
                    self.add_clean_words(sent.number_of_clean_words)
                text_features['Number of offensive words'] = self.total_number_of_offensive_words
                text_features['Number of clean words'] = self.total_number_of_clean_words
            # print(str(text_features))
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

    def get_category_rating(self, category: str):
        """
        This function provides the category rating for a given category.
        :param category: The category to return the rating for.
        :return: The category's rating, an int 1-10
        """
        return self.category_ratings[category]

    def get_category_word_counts(self, category: str):
        """
        This function provides a dictionary containing the words and word counts for a given category.
        :param category: The category to return the information for.
        :return: A dictionary containing the category's offensive words and their counts.
        """
        return self.category_word_counts[category]

    # def get_offensive_words_per_category(self, category: str):
    #     for key, value in self.total_strongly_offensive_words_dict.items():
    #         split_key = key.split(':')
    #         word = split_key[0]
    #         word_category = split_key[1]
    #         if word_category.lower() == category.lower():
    #             print()

    def calculate_offensive_ratio(self, numerator: int):
        """
        Calculates the ratio given the numerator and the denominator will be the total number of words in the document.
        This value is multiplied by 10 to provide a number between 0-10.
        :param numerator: An int, the numerator value.
        :return: The numerator divided by the total words, times 10.
        """
        return numerator / (self.total_number_of_clean_words + self.total_number_of_offensive_words) * 10

    def generate_category_ratings(self):
        """
        This function generates the category rating for every category in the database.
        :return: None
        """
        for category in model_helper.get_categories():
            strongly_offensive_category_words = 0
            for word, word_count in self.category_word_counts[category.name].items():
                strongly_offensive_category_words += word_count
            ratio = self.calculate_offensive_ratio(strongly_offensive_category_words)
            ratio = int(ratio) % 10 + 1
            self.category_ratings[category.name] = ratio

    def generate_rating(self):
        """
        This function generates an offensiveness rating using the text's classification data.
        :return: None.
        """
        strongly_offensive_word_rate = self.calculate_offensive_ratio(self.total_number_of_offensive_words)
        self.overall_rating = int(strongly_offensive_word_rate) % 10 + 1
        self.generate_category_ratings()
