from django.db.models import Model, ForeignKey, ManyToManyField, Manager, CASCADE
from django.contrib.auth.models import User
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.category import Category


class UserStorage(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    ratings = ManyToManyField(
        ContentRating, related_name='user_storage',
        blank=True)
    word_features = ManyToManyField(
        WordFeature, related_name='user_storage',
        blank=True)
    categories = ManyToManyField(
        Category, related_name='user_storage', blank=True)
    user_storage = Manager()

    class Meta:
        default_manager_name = 'user_storage'
