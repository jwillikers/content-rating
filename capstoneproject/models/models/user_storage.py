from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Model, OneToOneField, ManyToManyField, Manager, \
    CASCADE
from django.contrib.auth.models import User
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word import Word


class UserStorage(Model):
    def default_categories():
        return Category.categories.filter(default=True)

    def default_words():
        return Word.words.filter(default=True)

    def default_word_features():
        return WordFeature.word_features.filter(default=True)

    user = OneToOneField(User, on_delete=CASCADE)
    categories = ManyToManyField(
        Category,
        related_name='user_storage',
        blank=True,
        default=default_categories)
    words = ManyToManyField(
        Word,
        related_name='user_storage',
        blank=True,
        default=default_words)
    word_features = ManyToManyField(
        WordFeature,
        related_name='user_storage',
        blank=True,
        default=default_word_features)
    ratings = ManyToManyField(
        ContentRating,
        related_name='user_storage',
        blank=True)
    user_storage = Manager()

    @receiver(post_save, sender=User)
    def create_user_storage(sender, instance, created, **kwargs):
        if created:
            UserStorage.user_storage.create(
                user=instance, id=instance.id)

    class Meta:
        default_manager_name = 'user_storage'
