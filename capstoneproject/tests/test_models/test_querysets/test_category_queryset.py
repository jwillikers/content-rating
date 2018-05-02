from django.test import TestCase
from django.contrib.auth.models import User
from capstoneproject.models.querysets.category_queryset \
    import CategoryQuerySet
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.user_storage import UserStorage


class CategoryQuerySetTestClass(TestCase):
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
            name='test_category5', weight=1, default=True)
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

    def test_of_user(self):
        results = Category.categories.of_user(self.user1.id)
        self.assertIn(self.cat1, results)
        self.assertIn(self.cat2, results)
        self.assertIn(self.cat3, results)
        self.assertNotIn(self.cat4, results)
        self.assertIn(self.cat5, results)
