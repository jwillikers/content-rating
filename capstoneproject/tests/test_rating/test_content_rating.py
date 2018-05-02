from unittest import TestCase
from capstoneproject.content_rating.algorithm.content_rating import isalphanum
from capstoneproject.content_rating.algorithm.content_rating import ContentRatingAlgorithm
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory

class TestIsalphanum(TestCase):

    def test_isalphanum_letter(self):
            self.assertTrue(isalphanum('c'))
            self.assertTrue(isalphanum('dc'))
            self.assertFalse(isalphanum(' c'))

    def test_isalphanum_number(self):
            self.assertTrue(isalphanum('1'))
            self.assertTrue(isalphanum('12'))
            self.assertFalse(isalphanum(' 1'))

    def test_isalphanum_false(self):
            self.assertFalse(isalphanum(' '))
            self.assertFalse(isalphanum('---'))
            self.assertFalse(isalphanum('+'))
            self.assertFalse(isalphanum('?'))


class TestTokenize(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cr = ContentRatingAlgorithm()
        cls.factory = RequestFactory()
        cls.user = AnonymousUser()

    def test_tokenize_words(self):
        sentence_words = list()
        sentence_tokens = \
            TestTokenize.cr.tokenize('Hello World!', 1, self.user)[0].sentence_tokens
        for token in sentence_tokens:
            sentence_words.append(token[0])
        self.assertListEqual(sentence_words, ['Hello', 'World'])
