from django.test import TestCase
from django.contrib.auth.models import User
from capstoneproject.models.models.user_storage import UserStorage
from capstoneproject.models.models.word import Word
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.content import Content
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.category_rating import CategoryRating
from capstoneproject.models.models.word_count import WordCount


class UserStorageTestClass(TestCase):
    def setUp(self):
        self.category1 = Category.categories.create(
            default=True,
            name='category1',
            weight=1)
        self.word1 = Word.words.create(
            default=True,
            name='word1')
        self.word_feature1 = WordFeature.word_features.create(
            default=True,
            category=self.category1,
            strength=True,
            weight=1)

        self.user = User.objects.create(username='user1', password='123456')
        self.user.save()
        self.user_storage = UserStorage.user_storage.get(user=self.user.id)

    def tearDown(self):
        if self.user_storage.id is not None:
            self.user_storage.delete()
        if self.user.id is not None:
            self.user.delete()
        Word.words.all().delete()
        Category.categories.all().delete()
        WordFeature.word_features.all().delete()
        ContentRating.content_ratings.all().delete()
        Content.content.all().delete()
        CategoryRating.category_ratings.all().delete()
        WordCount.word_counts.all().delete()
        UserStorage.user_storage.all().delete()

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
        user_word.save()

        user_content = Content.content.create(title='Title', creator='Creator')
        user_content_rating = ContentRating.content_ratings.create(
            content=user_content)
        user_word_count = WordCount.word_counts.create(
            word=user_word, count=10)
        user_content_rating.word_counts.add(user_word_count)
        user_category_rating = CategoryRating.category_ratings.create(
            category=user_category, rating=5)
        user_content_rating.category_ratings.add(user_category_rating)
        self.user_storage.ratings.add(user_content_rating)
        self.user_storage.save()

        self.assertIn(
            user_word,
            Word.words.all(),
            msg='Word user_word should exist')
        self.assertIn(
            user_word,
            self.user_storage.words.all(),
            msg='Word user_word should belong to the user')
        self.assertIn(
            user_category,
            Category.categories.all(),
            msg='Category user_category should exist')
        self.assertIn(
            user_category,
            self.user_storage.categories.all(),
            msg='Category user_category should belong to the user')
        self.assertIn(
            user_feature,
            WordFeature.word_features.all(),
            msg='WordFeature user_feature should exist')
        self.assertIn(
            user_feature,
            self.user_storage.word_features.all(),
            msg='WordFeature user_feature should belong to the user')
        self.assertIn(
            user_content,
            Content.content.all(),
            msg='Content user_content should exist')
        self.assertEqual(
            user_content,
            user_content_rating.content,
            msg='Content user_content should exist')
        self.assertIn(
            user_word_count,
            WordCount.word_counts.all(),
            msg='WordCount user_word_count should exist')
        self.assertIn(
            user_word_count,
            user_content_rating.word_counts.all(),
            msg='WordCount user_word_count should be \
            related to the ContentRating model')
        self.assertIn(
            user_category_rating,
            CategoryRating.category_ratings.all(),
            msg='CategoryRating user_category_rating should exist')
        self.assertIn(
            user_category_rating,
            user_content_rating.category_ratings.all(),
            msg='CategoryRating user_category_rating should \
            be related to the ContentRating model')
        self.assertIn(
            user_content_rating,
            ContentRating.content_ratings.all(),
            msg='ContentRating user_content_rating should exist')
        self.assertIn(
            user_content_rating,
            self.user_storage.ratings.all(),
            msg='ContentRating user_content_rating should belong to the user')
        self.user_storage.delete_relatives()
        self.assertNotIn(
            user_word,
            Word.words.all(),
            msg='Word user_word was not deleted')
        self.assertNotIn(
            user_word,
            self.user_storage.words.all(),
            msg='Word user_word was not removed from UserStorage')
        self.assertNotIn(
            user_category,
            Category.categories.all(),
            msg='Category user_category should not exist')
        self.assertNotIn(
            user_category,
            self.user_storage.categories.all(),
            msg='Category user_category was not removed from UserStorage')
        self.assertNotIn(
            user_feature,
            WordFeature.word_features.all(),
            msg='WordFeature user_feature should not exist')
        self.assertNotIn(
            user_feature,
            self.user_storage.word_features.all(),
            msg='WordFeature user_feature was not removed from UserStorage')
        self.assertNotIn(
            user_content,
            Content.content.all(),
            msg='Content user_content should not exist')
        self.assertNotEqual(
            user_content,
            ContentRating.content,
            msg='Content user_content should not be related to ContentRating')
        self.assertNotIn(
            user_word_count,
            WordCount.word_counts.all(),
            msg='WordCount user_word_count should not exist')
        self.assertNotIn(
            user_word_count,
            user_content_rating.word_counts.all(),
            msg='WordCount user_word_count should not be \
            related to the ContentRating model')
        self.assertNotIn(
            user_category_rating,
            CategoryRating.category_ratings.all(),
            msg='CategoryRating user_category_rating should not exist')
        self.assertNotIn(
            user_category_rating,
            user_content_rating.category_ratings.all(),
            msg='CategoryRating user_category_rating should \
            not be related to the ContentRating table')
        self.assertNotIn(
            user_content_rating,
            ContentRating.content_ratings.all(),
            msg='ContentRating user_content_rating should not exist')
        self.assertNotIn(
            user_content_rating,
            self.user_storage.ratings.all(),
            msg='ContentRating user_content_rating should \
            not belong to the user')
