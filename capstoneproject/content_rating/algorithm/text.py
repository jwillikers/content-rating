"""
This file contains the Text class to contain data on the classification
and rating of a given text.
"""
from capstoneproject.helpers import model_helper
from django.contrib.auth.models import User

class Text:
    """
    Class to represent the text to classify and rate.
    """

    def __init__(self, text_sentences):
        """
        Initialize a Text object
        :param text_sentences: the sentences contained within the text, a list of Sentence objects.
        """
        self.title = ''     # Title of content
        self.creator = ''   # Creator/Author of content
        self.content_type = 4  # Type of content being rating
        self.offensive_sentences = dict()       # Keys are sentence indices, values are lists
                                                # of sentences's offensive categories
        self.sentence_list = text_sentences     # List of sentences in the text
        self.total_strongly_offensive_words_dict = dict()   # Keys are category names, values are dictionaries with
                                                            # offensive words as keys and counts as values
        self.total_weakly_offensive_words_dict = dict()     # Keys are category name, values are dictionaries with
                                                            # offensive words as keys and counts as values
        self.total_number_of_clean_words = 0        # Number of clean words in the text
        self.total_number_of_offensive_words = 0    # Number of offensive words in the text
        self.overall_rating = 1                     # Overall offensiveness rating
        self.category_ratings = dict()              # Keys are category name, values are category offensiveness rating
        self.category_word_counts = dict()          # Keys are category name, values are dictionaries with
                                                    # offensive words as keys and counts as values
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
        Initialize the category_ratings, category_word_counts,
        total_strongly_offensive_words, and total_weakly_offensive_words
        dictionaries to have the keys be the names of all categories,
        and each value is another dictionary.
        :return: None.
        """
        for category in model_helper.get_categories():
            self.category_ratings['{}'.format(category.name)] = 1
            self.category_word_counts['{}'.format(category.name)] = dict()
            self.total_strongly_offensive_words_dict['{}'.format(category.name)] = dict()
            self.total_weakly_offensive_words_dict['{}'.format(category.name)] = dict()
        self.overall_rating = 0

    def add_strongly_offensive_words(self, offensive_words: dict):
        """
        Use a dictionary of strongly offensive words and their quantities
        from a single sentence to update the text's total count.
        :param offensive_words: A dictionary where the key contains the
        strongly offensive word and its category and the value is the
        number of times the word occurred within a sentence.
        :return: None
        """
        for category, value in offensive_words.items():
            for word, word_count in offensive_words[category].items():
                try:
                    self.category_word_counts[category][word] += word_count
                except KeyError:
                    self.category_word_counts[category][word] = word_count

    def add_weakly_offensive_words(self, offensive_words: dict):
        """
        Use a dictionary of weakly offensive words and their quantities
        from a single sentence to update the text's total count.
        :param offensive_words: A dictionary where the key contains the
        weakly offensive word and its category and the value is the
        number of times the word occurred within a sentence.
        :return: None.
        """
        for category, value in offensive_words.items():
            for word, word_count in offensive_words[category].items():
                try:
                    self.category_word_counts[category][word] += word_count
                except KeyError:
                    self.category_word_counts[category][word] = word_count

    def add_offensive_words(self, number_of_offensive_words: int):
        """
        Update the text's total number of offensive words by adding the given amount.
        :param number_of_offensive_words: The number of offensive words to
        increase the total number of offensive words by.
        :return: None.
        """
        self.total_number_of_offensive_words += number_of_offensive_words

    def add_clean_words(self, number_of_clean_words: int):
        """
        Update the text's total number of clean words by adding the given amount.
        :param number_of_clean_words: The number of clean words to
        increase the total number of clean words by.
        :return: None.
        """
        self.total_number_of_clean_words += number_of_clean_words

    def update_offensive_sentences(self, sent_num: int, offensive_categories: list):
        """
        This function updates the dictionary of offensive sentences
        to set the value at the key given by the sentence index to map
        to a list of offensive categories that the sentence violates.
        :param sent_num: An int, the sentence index in the original document.
        :param offensive_categories: A list, containing strings of names of categories
        that the sentence is classified as.
        :return: None
        """
        self.offensive_sentences[sent_num] = offensive_categories

    def extract_features(self):
        """
        This function extracts the lexical and syntactic
        features from each sentence.
        :return: None.
        """
        text_features = {}
        for sent in self.sentence_list:
            sent.extract_lexical_features()  # Extract the lexical features from each sentence.
            print(sent)
            feature_file.write(str(sent) + '\n\n')
            # sent.extract_syntactic_features()  # Extract the syntactic features from each sentence.
            self.add_strongly_offensive_words(sent.strongly_offensive_words)
            self.add_weakly_offensive_words(sent.weakly_offensive_words)
            self.add_offensive_words(sent.number_of_offensive_words)
            self.add_clean_words(sent.number_of_clean_words)
            self.update_offensive_sentences(sent_num=sent.sentence_number, offensive_categories=sent.offensive_categories)
        text_features['Number of offensive words'] = self.total_number_of_offensive_words
        text_features['Number of clean words'] = self.total_number_of_clean_words
        # print(str(text_features))

    def get_text_features(self):
        """
        This function provides the offensive features of the text.
        :return: None
        """
        print("To do")

    def calculate_offensiveness(self):
        """
        This function calculates the offensiveness of each
        sentence within the text.
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
        This function provides a dictionary containing the words
        and word counts for a given category.
        :param category: The category to return the information for.
        :return: A dictionary containing the category's offensive
        words and their counts.
        """
        return self.category_word_counts[category]

    def get_word_counts(self):
        """
        This function returns a dictionary of all offensive words and
        their occurrences in the document, ignoring categories.
        :return: A dictionary where the key is the name of the offensive word
        and the value is the number of occurrences of the word in the document.
        """
        word_counts = dict()
        for category, value in self.category_word_counts.items():
            for word, count in value.items():
                word_counts[word] = count
        return word_counts

    # def get_offensive_words_per_category(self, category: str):
    #     for key, value in self.total_strongly_offensive_words_dict.items():
    #         split_key = key.split(':')
    #         word = split_key[0]
    #         word_category = split_key[1]
    #         if word_category.lower() == category.lower():
    #             print()

    def calculate_offensive_ratio(self, numerator: int):
        """
        Calculates the ratio given the numerator and the denominator
        will be the total number of words in the document.
        This value is multiplied by 10 to provide a number between 0-10.
        :param numerator: An int, the numerator value.
        :return: The numerator divided by the total words, times 10.
        """
        clean_words_fraction = int(self.total_number_of_clean_words/10)
        if clean_words_fraction <= self.total_number_of_offensive_words:
            clean_words_fraction = self.total_number_of_clean_words
        return numerator / (clean_words_fraction + self.total_number_of_offensive_words) * 10

    def _generate_category_ratings(self):
        """
        This function generates the category rating for
        every category in the database.
        :return: None
        """
        for category in model_helper.get_categories():
            strongly_offensive_category_words = 0
            for word, word_count in self.category_word_counts[category.name].items():
                strongly_offensive_category_words += word_count
            ratio = self.calculate_offensive_ratio(strongly_offensive_category_words)
            ratio = int(ratio) % 10 + 1
            self.category_ratings[category.name] = ratio

    def _generate_overall_rating(self, user: User):
        """
        This function generates the overall rating for the text using user's
        category weights. The overall rating is an int between 1-10.
        :param user: An User
        :return: None.
        """
        # strongly_offensive_word_rate = self._calculate_offensive_ratio(self.total_number_of_offensive_words)
        # self.overall_rating = int(strongly_offensive_word_rate) % 10 + 1

        max_rate = 10 * model_helper.get_num_categories()
        rate_total = 0

        for cat, rate in self.category_ratings.items():
            cat_weight = model_helper.get_category(category_name=cat).weight
            # get_user_category_weight(user=user, category_name=cat) + 1
            rate_total += cat_weight * rate

        if rate_total > 0:
            print(rate_total)
            print(max_rate)
            self.overall_rating = int(10 * rate_total / max_rate)
        else:
            self.overall_rating = 1

    def generate_rating(self, user:User):
        """
        This function generates an offensiveness rating using the text's classification data.
        :return: None.
        """
        self._generate_overall_rating(user)
        self._generate_category_ratings(user)
        print(self.overall_rating)
