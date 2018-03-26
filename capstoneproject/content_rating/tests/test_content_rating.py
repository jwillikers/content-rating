import unittest
from content_rating import isalphanum

class TestIsalphanum(unittest.TestCase):
    
    def test_isalphanum_letter():
            self.assertTrue(isalphanum('c'))
            self.assertTrue(isalphanum('dc'))
            self.assertTrue(isalphanum(' c'))

    def test_isalphanum_number():
            self.assertTrue(isalphanum('1'))
            self.assertTrue(isalphanum('12'))
            self.assertTrue(isalphanum(' 1'))
            self.assertTrue(isalphanum('=-/1'))

    def test_isalphanum_false():
            self.assertFalse(isalphanum(' '))
            self.assertFalse(isalphanum('---'))
            self.assertFalse(isalphanum('+'))
            self.assertFalse(isalphanum('?'))
