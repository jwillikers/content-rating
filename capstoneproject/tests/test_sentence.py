from unittest import TestCase
from nltk import pos_tag
from capstoneproject.content_rating.algorithm.sentence import Sentence

class TestSentenceAddStronglyOffensiveWord(TestCase):
    def setUp(self):
        self.sentence = Sentence([('hello'), ('world')], 0)
        self.sentence.add_strongly_offensive_word('shit', 'excretory')

    def test_word_count(self):
        self.assertDictEqual(self.sentence.strongly_offensive_words,
                             {'shit:excretory': 1})

    def test_added_category(self):
        self.assertListEqual(self.sentence.offensive_categories,
                             ['excretory'])

class TestSentenceAddWeaklyOffensiveWord(TestCase):
    def setUp(self):
        self.sentence = Sentence([('hello'), ('world')], 0)
        self.sentence.add_weakly_offensive_word('darn', 'oath')

    def test_word_count(self):
        self.assertDictEqual(self.sentence.weakly_offensive_words,
                             {'darn:oath': 1})

    def test_not_added_category(self):
        self.assertListEqual(self.sentence.offensive_categories,
                             [])
