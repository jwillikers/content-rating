from django.test import TestCase
from django.contrib.auth.models import User
from capstoneproject.models.db_queries.words_and_features \
    import words_and_features
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.user_storage import UserStorage


class WordsAndFeaturesTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat1 = Category.categories.create(
            name='test_category1', weight=1, default=True)
        cls.cat2 = Category.categories.create(
            name='test_category2', weight=2, default=True)
        cls.feature1 = WordFeature.word_features.create(
            default=True, category=cls.cat1, strength=True, weight=1)
        cls.feature2 = WordFeature.word_features.create(
            default=True, category=cls.cat2, strength=False, weight=3)
        cls.feature4 = WordFeature.word_features.create(
            default=True, category=cls.cat1, strength=True, weight=2)
        cls.feature5 = WordFeature.word_features.create(
            default=False, category=cls.cat1, strength=False, weight=1)
        cls.word1 = Word.words.create(name='word1', default=True)
        cls.word1.word_features.add(cls.feature1.id)
        cls.word2 = Word.words.create(name='word2', default=True)
        cls.word2.word_features.add(cls.feature2.id)
        cls.word3 = Word.words.create(name='word3', default=True)
        cls.word3.word_features.add(cls.feature1.id)
        cls.word3.word_features.add(cls.feature2.id)
        cls.word4 = Word.words.create(name='word4', default=True)
        cls.word4.word_features.add(cls.feature4.id)
        cls.word5 = Word.words.create(name='word5', default=False)
        cls.word5.word_features.add(cls.feature5.id)
        cls.word1.save()
        cls.word2.save()
        cls.word3.save()
        cls.word4.save()
        cls.word5.save()
        cls.user1 = User.objects.create_user(
            username='user1', password='12345')
        cls.user1.save()
        cls.user2 = User.objects.create_user(
            username='user2', password='12346')
        cls.user2.save()
        cls.user_storage1 = UserStorage.user_storage.get(user=cls.user1)
        cls.user_storage1.words.add(cls.word1)
        cls.user_storage1.words.add(cls.word2)
        cls.user_storage1.words.add(cls.word3)
        cls.user_storage1.categories.add(cls.cat1)
        cls.user_storage1.categories.add(cls.cat2)
        cls.user_storage1.word_features.add(cls.feature1)
        cls.user_storage1.word_features.add(cls.feature2)
        cls.user_storage1.save()
        cls.user_storage2 = UserStorage.user_storage.get(user=cls.user2)
        cls.user_storage2.words.add(cls.word1)
        cls.user_storage2.words.add(cls.word2)
        cls.user_storage2.words.add(cls.word3)
        cls.user_storage2.words.add(cls.word5)
        cls.user_storage2.categories.add(cls.cat1)
        cls.user_storage2.categories.add(cls.cat2)
        cls.user_storage2.word_features.add(cls.feature1)
        cls.user_storage2.word_features.add(cls.feature2)
        cls.user_storage2.word_features.add(cls.feature5)
        cls.user_storage2.save()

    @classmethod
    def tearDownClass(cls):
        Category.categories.all().delete()
        Word.words.all().delete()
        WordFeature.word_features.all().delete()
        UserStorage.user_storage.all().delete()
        User.objects.all().delete()

    def test_args_none(self):
        results = words_and_features()
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 3)
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'word_id': self.word1.id,
             'word': self.word1.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word1')
        self.assertIn(
            {'word_id': self.word2.id,
             'word': self.word2.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results, msg='missing word2')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word3, feature1')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results, msg='missing word3, feature2')
        self.assertIn(
            {'word_id': self.word4.id,
             'word': self.word4.name,
             'category_id': self.feature4.category.id,
             'strength': self.feature4.strength,
             'weight': self.feature4.weight},
            results, msg='missing word4')
        self.assertIn(
            {'word_id': self.word5.id,
             'word': self.word5.name,
             'category_id': self.feature5.category.id,
             'strength': self.feature5.strength,
             'weight': self.feature5.weight},
            results, msg='missing word5')

    def test_arg_user_id(self):
        results = words_and_features(user_id=self.user1.id)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 3)
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'word_id': self.word1.id,
             'word': self.word1.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word1')
        self.assertIn(
            {'word_id': self.word2.id,
             'word': self.word2.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results, msg='missing word2')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word3, feature1')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results, msg='missing word3, feature2')
        self.assertNotIn(
            {'word_id': self.word4.id,
             'word': self.word4.name,
             'category_id': self.feature4.category,
             'strength': self.feature4.strength,
             'weight': self.feature4.weight},
            results, msg='contains word4 which is not linked to this user')
        self.assertNotIn(
            {'word_id': self.word5.id,
             'word': self.word5.name,
             'category_id': self.feature5.category.id,
             'strength': self.feature5.strength,
             'weight': self.feature5.weight},
            results, msg='should not contain word5 which belongs to user2')

    def test_arg_category_id(self):
        results = words_and_features(category_id=self.cat1.id)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 3)
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'word_id': self.word1.id,
             'word': self.word1.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word1')
        self.assertNotIn(
            {'word_id': self.word2.id,
             'word': self.word2.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='contains category 2 word when it should not')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word3, feature1')
        self.assertNotIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='contains category 2 feature in word 3 when it should not')
        self.assertIn(
            {'word_id': self.word4.id,
             'word': self.word4.name,
             'category_id': self.feature4.category.id,
             'strength': self.feature4.strength,
             'weight': self.feature4.weight},
            results, msg='missing word4')
        self.assertIn(
            {'word_id': self.word5.id,
             'word': self.word5.name,
             'category_id': self.feature5.category.id,
             'strength': self.feature5.strength,
             'weight': self.feature5.weight},
            results,
            msg='missing word5')

    def test_arg_strength(self):
        results = words_and_features(strength=True)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 3)
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'word_id': self.word1.id,
             'word': self.word1.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word1')
        self.assertNotIn(
            {'word_id': self.word2.id,
             'word': self.word2.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='contains word2 of Strength = False when it should not')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word3, feature1')
        self.assertNotIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='''contains Strength = False feature in word3 when it should not
            ''')
        self.assertNotIn(
            {'word_id': self.word4.id,
             'word': self.word4.name,
             'category_id': self.feature4.category,
             'strength': self.feature4.strength,
             'weight': self.feature4.weight},
            results,
            msg='''contains word4 with Strength = False''')
        self.assertNotIn(
            {'word_id': self.word5.id,
             'word': self.word5.name,
             'category_id': self.feature5.category.id,
             'strength': self.feature5.strength,
             'weight': self.feature5.weight},
            results,
            msg='contains word5 of Strength = False when it should not')

    def test_arg_user_id_and_category_id(self):
        results = words_and_features(
            user_id=self.user1.id,
            category_id=self.cat1.id)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 3)
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertNotIn(
            {'word_id': self.word4.id,
             'word': self.word4.name,
             'category_id': self.feature4.category,
             'strength': self.feature4.strength,
             'weight': self.feature4.weight},
            results, msg='contains word4 which is not linked to this user')
        self.assertIn(
            {'word_id': self.word1.id,
             'word': self.word1.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word1')
        self.assertNotIn(
            {'word_id': self.word2.id,
             'word': self.word2.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='contains category 2 word when it should not')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word3, feature1')
        self.assertNotIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='contains category 2 feature in word 3 when it should not')
        self.assertNotIn(
            {'word_id': self.word4.id,
             'word': self.word4.name,
             'category_id': self.feature4.category,
             'strength': self.feature4.strength,
             'weight': self.feature4.weight},
            results, msg='contains word4 which is not linked to this user')
        self.assertNotIn(
            {'word_id': self.word5.id,
             'word': self.word5.name,
             'category_id': self.feature5.category.id,
             'strength': self.feature5.strength,
             'weight': self.feature5.weight},
            results,
            msg='contains word5 that does not belong to user1')

    def test_args_all(self):
        results = words_and_features(
            user_id=self.user1.id,
            category_id=self.cat1.id,
            strength=self.feature1.strength)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 3)
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'word_id': self.word1.id,
             'word': self.word1.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word1')
        self.assertNotIn(
            {'word_id': self.word2.id,
             'word': self.word2.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='''contains word2 of Strength = False and category2 when it should not
            ''')
        self.assertIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat1.id,
             'strength': self.feature1.strength,
             'weight': self.feature1.weight},
            results, msg='missing word3, feature1')
        self.assertNotIn(
            {'word_id': self.word3.id,
             'word': self.word3.name,
             'category_id': self.cat2.id,
             'strength': self.feature2.strength,
             'weight': self.feature2.weight},
            results,
            msg='''contains Strength = False and category2 feature in word3 when it should not
            ''')
        self.assertNotIn(
            {'word_id': self.word5.id,
             'word': self.word5.name,
             'category_id': self.feature5.category.id,
             'strength': self.feature5.strength,
             'weight': self.feature5.weight},
            results,
            msg='''contains word5 of Strength = False that does not belong
            to user1''')
