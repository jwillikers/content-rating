from django.test import TestCase
from django.contrib.auth.models import User
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word_feature import WordFeature


class UserStorageTestClass(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', password='123456')
        self.user.save()
        self.user_storage = UserStorage.user_storage.get(user=self.user.id)

    def tearDown(self):
        self.user_storage.delete()
        self.user.delete()

    def test_autocreate(self):
        self.assertIsNotNone(
            self.user_storage,
            msg="UserStorage with user's pk was not created")
        default_words = list(Word.words.filter(default=True).all())
        user_words = list(self.user_storage.words.all())
        self.assertListEqual(
            user_words,
            default_words,
            msg="User's Words do not match default Words")
        default_categories = list(Category.categories.filter(
            default=True).all())
        user_categories = list(self.user_storage.categories.all())
        self.assertListEqual(
            user_categories,
            default_categories,
            msg="User's categories do not match default Categories")
        default_features = list(WordFeature.word_features.filter(
            default=True).all())
        user_features = list(self.user_storage.word_features.all())
        self.assertListEqual(
            user_features,
            default_features,
            msg="User's WordFeatures do not match default WordFeatures")
