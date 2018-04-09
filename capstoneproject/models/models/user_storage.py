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
    """
    This Model contains data that is specific to each user.
    """
    def default_categories(self):
        """
        Returns the default Categories from the database.
        :return: A list of all Categories.
        """
        return Category.categories.filter(default=True).all()

    def default_words(self):
        """
        Returns all default Words from the database.
        :return: A list of all Words
        """
        return Word.words.filter(default=True).all()

    def default_word_features(self):
        """
        Returns all default Word Features from the database.
        :return: A list of all Word Features
        """
        return WordFeature.word_features.filter(default=True).all()

    def __str__(self):
        string = 'User Storage:\n'
        string += '  User: {}\n'.format(self.user.username)
        string += '  Ratings: {}\n'.format(self.ratings)
        string += '  Word Features: {}\n'.format(self.word_features)
        string += '  Categories: {}\n'.format(self.categories)
        return string

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
        """
        This method creates a new user storage model.
        :param instance:
        :param created:
        :param kwargs:
        :return:
        """
        if created:
            UserStorage.user_storage.create(
                user=instance, id=instance.id)

    class Meta:
        default_manager_name = 'user_storage'
