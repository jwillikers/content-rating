from django.test import TestCase
from django.contrib.auth.models import User
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word_feature import WordFeature


class UserStorageTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.category1 = Category.categories.create(
            default=True,
            name='category1',
            weight=1)
        cls.word1 = Word.words.create(
            default=True,
            name='word1')
        cls.word_feature1 = WordFeature.word_features.create(
            default=True,
            category=cls.category1,
            strength=True,
            weight=1)

    @classmethod
    def tearDownClass(cls):
        Word.words.all().delete()
        Category.categories.all().delete()
        WordFeature.word_features.all().delete()

    def setUp(self):
        self.user = User.objects.create(username='user1', password='123456')
        self.user.save()
        self.user_storage = UserStorage.user_storage.get(user=self.user.id)

    def tearDown(self):
        if self.user_storage.id is not None:
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

    def test_delete_user_storage(self):
        self.assertIsNotNone(
            self.user_storage,
            msg="UserStorage with user's pk was not created")
        self.user_storage.delete()
        self.assertFalse(
            UserStorage.user_storage.filter(user=self.user.id).exists(),
            msg="The deleted UserStorage still exists")

    def test_delete_relatives(self):
        user_word = Word.words.create(name='user_word', default=False)
        self.user_storage.words.add(user_word)
        user_category = Category.categories.create(
            name='user_category', weight=1, default=False)
        self.user_storage.categories.add(user_category)
        user_feature = WordFeature.word_features.create(
                category=user_category, weight=1, strength=True, default=False)
        self.user_storage.word_features.add(user_feature)
        user_word.word_features.add(user_feature)
        self.assertTrue(
            Word.words.filter(
                id=user_word.id).exists(), msg='Word user_word should exist')
        self.assertTrue(
            Category.categories.filter(
                id=user_category.id).exists(),
            msg='Category user_category should exist')
        self.assertTrue(
            WordFeature.word_features.filter(
                id=user_feature.id).exists(),
            msg='WordFeature user_feature should exist')
        self.user_storage.delete_relatives()
        self.assertFalse(
            Word.words.filter(
                id=user_word.id).exists(),
            msg='Word user_word was not deleted')
        self.assertFalse(
            Category.categories.filter(
                id=user_category.id).exists(),
            msg='Category user_category should not exist')
        self.assertFalse(
            WordFeature.word_features.filter(
                id=user_feature.id).exists(),
            msg='WordFeature user_feature should not exist')

    def test_delete_user(self):
        pass
