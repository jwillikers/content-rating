from django.test import TestCase
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.word_feature import WordFeature


class TestWordQuerySet(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat1 = Category.categories.create(name='test_category1', weight=1)
        cls.cat2 = Category.categories.create(name='test_category2', weight=2)
        cls.feature1 = WordFeature.word_features.create(
            category=cls.cat1, strength=True, weight=1)
        cls.feature2 = WordFeature.word_features.create(
            category=cls.cat2, strength=False, weight=3)
        cls.feature4 = WordFeature.word_features.create(
            category=cls.cat1, strength=True, weight=2)
        cls.word1 = Word.words.create(name='word1')
        cls.word1.word_features.add(cls.feature1.id)
        cls.word2 = Word.words.create(name='word2')
        cls.word2.word_features.add(cls.feature2.id)
        cls.word3 = Word.words.create(name='word3')
        cls.word4 = Word.words.create(name='word4')
        cls.word3.word_features.add(cls.feature1.id)
        cls.word3.word_features.add(cls.feature2.id)
        cls.word4.word_features.add(cls.feature4.id)
        cls.word1.save()
        cls.word2.save()
        cls.word3.save()
        cls.word4.save()

    @classmethod
    def tearDownClass(cls):
        Category.categories.all().delete()
        Word.words.all().delete()
        WordFeature.word_features.all().delete()

    def test_category_name(self):
        cat1_name = TestWordQuerySet.cat1.name
        cat1_words = Word.words.category(cat1_name).all()
        self.assertIn(TestWordQuerySet.word1, cat1_words)
        self.assertNotIn(TestWordQuerySet.word2, cat1_words)
        self.assertIn(TestWordQuerySet.word3, cat1_words)

    def test_category_id(self):
        cat1_id = TestWordQuerySet.cat1.id
        cat1_words = Word.words.category(cat1_id).all()
        self.assertIn(TestWordQuerySet.word1, cat1_words)
        self.assertNotIn(TestWordQuerySet.word2, cat1_words)
        self.assertIn(TestWordQuerySet.word3, cat1_words)

    def test_category_object(self):
        cat1_words = Word.words.category(TestWordQuerySet.cat1).all()
        self.assertIn(TestWordQuerySet.word1, cat1_words)
        self.assertNotIn(TestWordQuerySet.word2, cat1_words)
        self.assertIn(TestWordQuerySet.word3, cat1_words)

    def test_category_bad_name(self):
        bad_category = 'not a real category'
        words = Word.words.category(bad_category).all()
        self.assertFalse(words)

    def test_category_type_error(self):
        with self.assertRaises(TypeError):
            Word.words.category(1.1)
        with self.assertRaises(TypeError):
            Word.words.category(TestWordQuerySet.word1)

    def test_category_prefetch_size(self):
        word3 = Word.words.category(TestWordQuerySet.cat1).get(name=TestWordQuerySet.word3.name)
        self.assertEqual(len(word3.word_features_list), 1)

    def test_category_prefetch(self):
        word3 = Word.words.category(TestWordQuerySet.cat1).get(name=TestWordQuerySet.word3.name)
        self.assertIn(TestWordQuerySet.feature1, word3.word_features_list)
        self.assertNotIn(TestWordQuerySet.feature2, word3.word_features_list)

    def test_category_chain(self):
        words = list(Word.words.category(TestWordQuerySet.cat1).category(TestWordQuerySet.cat2).all())
        self.assertIn(TestWordQuerySet.word3, words)
        self.assertNotIn(TestWordQuerySet.word1, words)
        self.assertNotIn(TestWordQuerySet.word2, words)

    def test_category_chain_prefetch(self):
        features = list(Word.words.category(TestWordQuerySet.cat1).category(TestWordQuerySet.cat2).get_word(TestWordQuerySet.word3).word_features_list)
        self.assertNotIn(TestWordQuerySet.feature1, features)
        self.assertIn(TestWordQuerySet.feature2, features)
        self.assertNotIn(TestWordQuerySet.feature4, features)

    def test_word_name(self):
        word1_name = TestWordQuerySet.word1.name
        word_words = Word.words.word(word1_name).all()
        self.assertIn(TestWordQuerySet.word1, word_words)
        self.assertNotIn(TestWordQuerySet.word2, word_words)
        self.assertNotIn(TestWordQuerySet.word3, word_words)

    def test_word_id(self):
        word1_id = TestWordQuerySet.word1.id
        word_words = Word.words.word(word1_id).all()
        self.assertIn(TestWordQuerySet.word1, word_words)
        self.assertNotIn(TestWordQuerySet.word2, word_words)
        self.assertNotIn(TestWordQuerySet.word3, word_words)

    def test_word_object(self):
        word1 = TestWordQuerySet.word1
        word_words = Word.words.word(word1).all()
        self.assertIn(TestWordQuerySet.word1, word_words)
        self.assertNotIn(TestWordQuerySet.word2, word_words)
        self.assertNotIn(TestWordQuerySet.word3, word_words)

    def test_word_bad_name(self):
        bad_word = 'not a real word'
        words = Word.words.word(bad_word).all()
        self.assertFalse(words)

    def test_word_type_error(self):
        with self.assertRaises(TypeError):
            Word.words.word(1.1)
        with self.assertRaises(TypeError):
            Word.words.word(TestWordQuerySet.cat1)

    def test_word_chain_not_words(self):
        not_words = Word.words.word('ass').word('fuck')
        self.assertFalse(not_words)

    def test_word_chain_words(self):
        words = Word.words.word(TestWordQuerySet.word1).word(TestWordQuerySet.word2)
        self.assertFalse(words)

    def test_word_category_chain(self):
        words = Word.words.category(TestWordQuerySet.cat1).word(TestWordQuerySet.word1)
        self.assertEqual(TestWordQuerySet.word1, words.first())

    def test_word_category_chain_prefetch(self):
        words = Word.words.category(TestWordQuerySet.cat1).word(TestWordQuerySet.word3)
        self.assertIn(TestWordQuerySet.feature1, list(words.first().word_features_list))
        self.assertNotIn(TestWordQuerySet.feature2, list(words.first().word_features_list))

    def test_strength_string(self):
        strong = Word.words.strength('strong').all()
        self.assertIn(TestWordQuerySet.word1, strong)
        self.assertNotIn(TestWordQuerySet.word2, strong)
        self.assertIn(TestWordQuerySet.word3, strong)

    def test_strength_string_uppercase(self):
        weak = Word.words.strength('WEAK').all()
        self.assertNotIn(TestWordQuerySet.word1, weak)
        self.assertIn(TestWordQuerySet.word2, weak)
        self.assertIn(TestWordQuerySet.word3, weak)

    def test_strength_bool(self):
        strong = Word.words.strength(True).all()
        self.assertIn(TestWordQuerySet.word1, strong)
        self.assertNotIn(TestWordQuerySet.word2, strong)
        self.assertIn(TestWordQuerySet.word3, strong)

    def test_strength_type_error(self):
        with self.assertRaises(TypeError):
            Word.words.strength(24)
        with self.assertRaises(TypeError):
            Word.words.strength(1.0)
        with self.assertRaises(TypeError):
            Word.words.strength(TestWordQuerySet.word1)

    def test_strength_prefetch_size(self):
        word3 = Word.words.strength(TestWordQuerySet.feature1.strength).get(name=TestWordQuerySet.word3.name)
        self.assertEqual(len(word3.word_features_list), 1)

    def test_strength_prefetch(self):
        word3 = Word.words.strength(TestWordQuerySet.feature1.strength).get(name=TestWordQuerySet.word3.name)
        self.assertIn(TestWordQuerySet.feature1, word3.word_features_list)
        self.assertNotIn(TestWordQuerySet.feature2, word3.word_features_list)

    def test_strength_chain(self):
        words = list(Word.words.strength(TestWordQuerySet.feature1.strength).strength(TestWordQuerySet.feature2.strength).all())
        self.assertIn(TestWordQuerySet.word3, words)
        self.assertNotIn(TestWordQuerySet.word1, words)
        self.assertNotIn(TestWordQuerySet.word2, words)
        self.assertNotIn(TestWordQuerySet.word4, words)

    def test_category_strength_prefetch_chain(self):
        word3 = Word.words.strength(TestWordQuerySet.feature1.strength).category(TestWordQuerySet.cat1.name).get(name=TestWordQuerySet.word3.name)
        self.assertIn(TestWordQuerySet.feature1, word3.word_features_list)
        self.assertNotIn(TestWordQuerySet.feature2, word3.word_features_list)

    def test_strength_value_error(self):
        with self.assertRaises(ValueError):
            Word.words.strength('over 9000')

    def test_weight_number(self):
        weight_1 = Word.words.weight(1).all()
        self.assertIn(TestWordQuerySet.word1, weight_1)
        self.assertNotIn(TestWordQuerySet.word2, weight_1)
        self.assertIn(TestWordQuerySet.word3, weight_1)

    def test_weight_string(self):
        weight_1 = Word.words.weight('slight').all()
        self.assertIn(TestWordQuerySet.word1, weight_1)
        self.assertNotIn(TestWordQuerySet.word2, weight_1)
        self.assertIn(TestWordQuerySet.word3, weight_1)

    def test_weight_string_uppercase(self):
        weight_3 = Word.words.weight('HEAVY').all()
        self.assertNotIn(TestWordQuerySet.word1, weight_3)
        self.assertIn(TestWordQuerySet.word2, weight_3)
        self.assertIn(TestWordQuerySet.word3, weight_3)

    def test_weight_empty(self):
        weight_0 = Word.words.weight(0).all()
        self.assertFalse(weight_0)

    def test_weight_type_error(self):
        with self.assertRaises(TypeError):
            Word.words.weight(1.0)
        with self.assertRaises(TypeError):
            Word.words.weight(TestWordQuerySet.word1)

    def test_weight_value_error(self):
        with self.assertRaises(ValueError):
            Word.words.weight('over 9000')
        with self.assertRaises(ValueError):
            Word.words.weight(9001)
        with self.assertRaises(ValueError):
            Word.words.weight(-1)
        with self.assertRaises(ValueError):
            Word.words.weight(4)

    def test_weight_prefetch_size(self):
        word3 = Word.words.weight(TestWordQuerySet.feature1.weight).get(name=TestWordQuerySet.word3.name)
        self.assertEqual(len(word3.word_features_list), 1)

    def test_weight_prefetch(self):
        word3 = Word.words.weight(TestWordQuerySet.feature1.weight).get(name=TestWordQuerySet.word3.name)
        self.assertIn(TestWordQuerySet.feature1, word3.word_features_list)
        self.assertNotIn(TestWordQuerySet.feature2, word3.word_features_list)

    def test_feature_prefetch_chain(self):
        word3 = Word.words.weight(TestWordQuerySet.feature1.weight).strength(TestWordQuerySet.feature1.strength).category(TestWordQuerySet.cat1.name).get(name=TestWordQuerySet.word3.name)
        self.assertIn(TestWordQuerySet.feature1, word3.word_features_list)
        self.assertNotIn(TestWordQuerySet.feature2, word3.word_features_list)

    def test_get_word_name(self):
        word1_name = TestWordQuerySet.word1.name
        word = Word.words.get_word(word1_name)
        self.assertEqual(TestWordQuerySet.word1, word)

    def test_get_word_id(self):
        word2_id = TestWordQuerySet.word2.id
        word = Word.words.get_word(word2_id)
        self.assertEqual(TestWordQuerySet.word2, word)

    def test_get_word_object(self):
        word3 = TestWordQuerySet.word3
        word = Word.words.get_word(word3)
        self.assertEqual(TestWordQuerySet.word3, word)

    def test_get_word_bad_name(self):
        bad_word = 'not a real word'
        word = Word.words.get_word(bad_word)
        self.assertIsNone(word)

    def test_get_word_type_error(self):
        with self.assertRaises(TypeError):
            Word.words.get_word(1.1)
        with self.assertRaises(TypeError):
            Word.words.get_word(TestWordQuerySet.cat1)
