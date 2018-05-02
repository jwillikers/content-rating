from django.test import TestCase
from django.contrib.auth.models import User
from capstoneproject.models.db_queries.categories \
    import categories
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.user_storage import UserStorage


class CategoriesTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat1 = Category.categories.create(
            name='test_category1', weight=1, default=True)
        cls.cat2 = Category.categories.create(
            name='test_category2', weight=2, default=True)
        cls.cat3 = Category.categories.create(
            name='test_category3', weight=3, default=False)
        cls.cat4 = Category.categories.create(
            name='test_category4', weight=0, default=False)
        cls.cat5 = Category.categories.create(
            name='test_category5', weight=1, default=False)
        cls.user1 = User.objects.create_user(
            username='user1', password='12345')
        cls.user1.save()
        cls.user2 = User.objects.create_user(
            username='user2', password='12346')
        cls.user2.save()
        cls.user_storage1 = UserStorage.user_storage.get(user=cls.user1)
        cls.user_storage1.categories.add(cls.cat1)
        cls.user_storage1.categories.add(cls.cat2)
        cls.user_storage1.categories.add(cls.cat3)
        cls.user_storage1.save()
        cls.user_storage2 = UserStorage.user_storage.get(user=cls.user2)
        cls.user_storage2.categories.add(cls.cat1)
        cls.user_storage2.categories.add(cls.cat2)
        cls.user_storage2.categories.add(cls.cat4)
        cls.user_storage2.save()

    @classmethod
    def tearDownClass(cls):
        Category.categories.all().delete()
        User.objects.all().delete()
        UserStorage.user_storage.all().delete()

    def test_args_none(self):
        results = categories()
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 1, msg='result list is empty')
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'id': self.cat1.id,
             'name': self.cat1.name,
             'weight': self.cat1.weight},
            results, msg='missing cat1')
        self.assertIn(
            {'id': self.cat2.id,
             'name': self.cat2.name,
             'weight': self.cat2.weight},
            results, msg='missing cat2')
        self.assertIn(
            {'id': self.cat3.id,
             'name': self.cat3.name,
             'weight': self.cat3.weight},
            results, msg='missing cat3')
        self.assertIn(
            {'id': self.cat4.id,
             'name': self.cat4.name,
             'weight': self.cat4.weight},
            results, msg='missing cat4')
        self.assertIn(
            {'id': self.cat5.id,
             'name': self.cat5.name,
             'weight': self.cat5.weight},
            results, msg='missing cat5')

    def test_arg_user_id(self):
        results = categories(user_id=self.user1.id)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 1, msg='result list is empty')
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'id': self.cat1.id,
             'name': self.cat1.name,
             'weight': self.cat1.weight},
            results, msg='missing cat1')
        self.assertIn(
            {'id': self.cat2.id,
             'name': self.cat2.name,
             'weight': self.cat2.weight},
            results, msg='missing cat2')
        self.assertIn(
            {'id': self.cat3.id,
             'name': self.cat3.name,
             'weight': self.cat3.weight},
            results, msg='missing cat3')
        self.assertNotIn(
            {'id': self.cat4.id,
             'name': self.cat4.name,
             'weight': self.cat4.weight},
            results, msg='cat4 does not belong to user1')
        self.assertNotIn(
            {'id': self.cat5.id,
             'name': self.cat5.name,
             'weight': self.cat5.weight},
            results, msg='cat5 does not belong to user1')

    def test_arg_default(self):
        results = categories(default=True)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 1, msg='result list is empty')
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'id': self.cat1.id,
             'name': self.cat1.name,
             'weight': self.cat1.weight},
            results, msg='missing cat1')
        self.assertIn(
            {'id': self.cat2.id,
             'name': self.cat2.name,
             'weight': self.cat2.weight},
            results, msg='missing cat2')
        self.assertNotIn(
            {'id': self.cat3.id,
             'name': self.cat3.name,
             'weight': self.cat3.weight},
            results, msg='non-default cat3 does not belong in the results')
        self.assertNotIn(
            {'id': self.cat4.id,
             'name': self.cat4.name,
             'weight': self.cat4.weight},
            results, msg='non-default cat4 does not belong in the results')
        self.assertNotIn(
            {'id': self.cat5.id,
             'name': self.cat5.name,
             'weight': self.cat5.weight},
            results, msg='missing cat5')

    def test_args_user_id_and_default(self):
        results = categories(user_id=self.user1.id, default=True)
        self.assertIsInstance(results, list, msg='result is not a list')
        self.assertGreaterEqual(len(results), 1, msg='result list is empty')
        self.assertIsInstance(
            results[0], dict,
            msg='result is not a list of dictionaries')
        self.assertIn(
            {'id': self.cat1.id,
             'name': self.cat1.name,
             'weight': self.cat1.weight},
            results, msg='missing cat1')
        self.assertIn(
            {'id': self.cat2.id,
             'name': self.cat2.name,
             'weight': self.cat2.weight},
            results, msg='missing cat2')
        self.assertNotIn(
            {'id': self.cat3.id,
             'name': self.cat3.name,
             'weight': self.cat3.weight},
            results, msg='non-default cat3 does not belong in the results')
        self.assertNotIn(
            {'id': self.cat4.id,
             'name': self.cat4.name,
             'weight': self.cat4.weight},
            results, msg='non-default cat4 does not belong in the results')
        self.assertNotIn(
            {'id': self.cat5.id,
             'name': self.cat5.name,
             'weight': self.cat5.weight},
            results, msg='cat5 does not belong to user1')
