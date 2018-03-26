from unittest import TestCase
from capstoneproject.content_rating.algorithm.content_rating import isalphanum

class TestIsalphanum(TestCase):

    def test_isalphanum_letter(self):
            self.assertTrue(isalphanum('c'))
            self.assertTrue(isalphanum('dc'))
            self.assertTrue(isalphanum(' c'))

    def test_isalphanum_number(self):
            self.assertTrue(isalphanum('1'))
            self.assertTrue(isalphanum('12'))
            self.assertTrue(isalphanum(' 1'))
            self.assertTrue(isalphanum('=-/1'))

    def test_isalphanum_false(self):
            self.assertFalse(isalphanum(' '))
            self.assertFalse(isalphanum('---'))
            self.assertFalse(isalphanum('+'))
            self.assertFalse(isalphanum('?'))
