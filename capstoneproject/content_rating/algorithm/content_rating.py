import nltk
import string

from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from capstoneproject.models import Category, Word, WordCategory
from capstoneproject.content_rating.spelling_correction import SpellChecker

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

    def __init__(self):
        self.spellchecker = SpellChecker()
        self.spellchecker.word_frequency.load_text_file('capstoneproject/testing_resources/Pillow_Talking')

        category_list = Category.objects.all()

    def lexical_features(self, sent_tokens):
        """
        This function derives lexical features from a tokenized sentence
        :param sent_tokens: a list of tuples. The first element is a word token, the second element is its POS tag.
        :return: a set of lexical features
        """
        features = {}

        non_dict_words = 0
        words = []
        for word, POS_tag in sent_tokens:
            words.append(word)
            if word not in Word.objects.all():
                non_dict_words += 1
        features['clean_words'] = non_dict_words
        # Make a feature for every category.
        for category in Category.objects.all():
            # Initially set the strongly_offensive feature for the current category to false.
            features['strongly_offensive({})'.format(str(category))] = False
            # For every offensive word that falls in that category, check if it is in the current sentence.
            for word in Word.objects.filter(word_category_set__category=category.id):
                contains = word.word in words
                # Update the sentence to be strongly offensive if a strongly offensive word is within the sentence.
                if contains and word.word_category_set.filter(category=category.id, weight=True):
                    features['strongly_offensive({})'.format(str(category))] = True
                # Flag the appearance of word in the dictionary and provide the number of counts.
                features['contains({}-{})'.format(str(category), word.word)] = contains
                features['count({}-{})'.format(str(category), word.word)] = words.count(word)

        return features

    def syntactic_features(self, sent_tokens):
        print("To Do")

    def tokenize(self, text):
        output_path = 'capstoneproject/testing_resources/Tokens'
        with open(output_path, 'w') as output_file:
            # Define Spell Checker
            tweet_tokenizer = TweetTokenizer(reduce_len=True)

            tokenized_sents = []
            for sent in nltk.sent_tokenize(text):
                words = [word for word in tweet_tokenizer.tokenize(sent) if isalphanum(word)]
                # words = [word for word in nltk.word_tokenize(sent) if word not in string.punctuation]
                # Spelling Correction
                spell_words = []
                for pos, word in enumerate(words):
                    unknown_words = self.spellchecker.unknown([word])
                    if len(unknown_words) > 0:
                        for misspell in unknown_words:
                            correct_spelling = self.spellchecker.correction(misspell)
                            spell_words.append(correct_spelling)
                    else:
                        spell_words.append(word)
                tokenized_sents.append(words)
            tagged_tokenized_text = nltk.pos_tag_sents(tokenized_sents)
            output_file.write(str(tagged_tokenized_text))
            return tagged_tokenized_text

    def algorithm(self, text):
        print("In algorithm")
        input_path = 'capstoneproject/testing_resources/Baby_Got_Back'
        with open(input_path, 'r') as input_file:
            text = input_file.read()
        # Normalize Text
        text = text.lower()
        tokenized_text = self.tokenize(text)
        # Extract Features
        features_path = 'capstoneproject/testing_resources/Features'
        with open(features_path, 'w') as feature_file:
            for sent in tokenized_text:
                featureset = self.lexical_features(sent)
                feature_file.write(str(featureset) + '\n\n')

