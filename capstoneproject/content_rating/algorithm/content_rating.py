"""
This file contains classes and function to implement the content
offensiveness classification and content rating algorithm.
"""
import nltk
import string
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from capstoneproject.content_rating.spelling_correction import SpellChecker
from capstoneproject.content_rating.algorithm.sentence import Sentence
from capstoneproject.content_rating.algorithm.text import Text


def isalphanum(word):
    """
    This function returns true if a word contains letters or digits
    :param word: A string token to check
    :return: True if the word contains letters or digits
    """
    for char in word:
        if char in string.ascii_letters or char in string.digits:
            return True
    return False


class ContentRating:
    """
    Class to implement the content rating algorithm and contain relevant methods.
    """
    def __init__(self):
        """
        Initialize the ContentRating class by initializing the spell checker.
        """
        self.spellchecker = SpellChecker()
        # Load extra texts to the dictionary used by the SpellChecker to make it more similar to the content that the
        # system will be exposed to.
        self.spellchecker.word_frequency.load_text_file('capstoneproject/testing_resources/Pillow_Talking')

    def correct_spelling(self, words):
        """"
        This function performs the spelling correction functionality by identifying words within a given sentence that
        do not appear within the dictionary. If the word does not appear, it corrects the word to its most probable
        match.
        :param words: A list containing the words within a sentence.
        :return: A list of the sentence's words with no typos.
        """
        spell_words = []  # A list to store the edited version of the sentence that fixes typos.
        for word in words:
            unknown_words = self.spellchecker.unknown([word])  # will be empty if the word is in the dictionary.
            if len(unknown_words) > 0:
                correct_spelling = self.spellchecker.correction(unknown_words.pop())
                spell_words.append(correct_spelling)  # Add the most likely correction of the word to the edited
                # sentence if it was a typo.
            else:
                spell_words.append(word)  # Add the original word to the edited sentence if it was not a typo.
        return spell_words

    def tokenize(self, text, content_type):
        """
        Perform the first phase of the content rating algorithm by tokenizing and normalizing the text.
        :param text: The text, given as a string, to tokenize and normalize.
        :return: The list of tokenized sentences.
        """
        # Use tweet tokenizer to tokenize individual words within sentences.
        # Reduce_len will compact words where letters occur 3 or more times due to typos.
        tweet_tokenizer = TweetTokenizer(reduce_len=True)
        sentences = []
        for count, sent in enumerate(nltk.sent_tokenize(text)):
            words = [word for word in tweet_tokenizer.tokenize(sent) if isalphanum(word)]
            if content_type == 3 or content_type == 4:
                words = self.correct_spelling(words)
            sentences.append(Sentence(words, count))
        #    tagged_tokenized_text = nltk.pos_tag_sents(tokenized_sents)
        print("\n\nSENTENCES:")
        for sent in sentences:
            print(sent)
        return sentences

    def algorithm(self, text_string, user, content_type):
        """
        Implement the offensive content classification and content rating algorithm.
        :param text_string: A string containing the text to classify and rate.
        :return: a Text object, containing the results.
        """
        # Step 1: Normalize, Tokenize, and perform Spelling Correction on Text
        text = Text(self.tokenize(text_string.lower(), content_type))

        # Step 2: Extract Features
        text.extract_features()

        # Step 3: Determine offensiveness
        # text.calculate_offensiveness()

        # Step 4: Generate rating
        text.generate_rating(user)

        return text
