from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.db.models import Model, OneToOneField, ManyToManyField, Manager, \
    CASCADE
from django.contrib.auth.models import User
from capstoneproject.models.models.content_rating import ContentRating
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word import Word
from capstoneproject.models.querysets.user_storage_queryset \
    import UserStorageQuerySet


class UserStorage(Model):
    """
    This Model contains data that is specific to each user.
    """
    user = OneToOneField(User, on_delete=CASCADE)
    categories = ManyToManyField(
        Category,
        related_name='user_storage',
        blank=True)
    words = ManyToManyField(
        Word,
        related_name='user_storage',
        blank=True)
    word_features = ManyToManyField(
        WordFeature,
        related_name='user_storage',
        blank=True)
    ratings = ManyToManyField(
        ContentRating,
        related_name='user_storage',
        blank=True)
    user_storage = UserStorageQuerySet.as_manager()

    def __str__(self):
        string = 'User Storage:\n'
        string += '  User: {}\n'.format(self.user.username)
        string += '  Ratings: {}\n'.format(self.ratings)
        string += '  Word Features: {}\n'.format(self.word_features)
        string += '  Categories: {}\n'.format(self.categories)
        return string

    @receiver(post_save, sender=User)
    def create_user_storage(sender, instance, created, **kwargs):
        """
        Creates a new user storage model upon
        creation of a new user.
        :param instance:
        :param created:
        :param kwargs:
        :return:
        """
        if created:
            UserStorage.user_storage.autocreate(instance)

    @receiver(post_delete, sender=User)
    def delete_user_storage(sender, instance, **kwargs):
        if instance and UserStorage.user_storage.filter(
                id=instance.id).exists():
            my_user_storage = UserStorage.user_storage.get(id=instance.id)
            my_user_storage.delete_relatives()
            my_user_storage.delete()

    def delete_relatives(self):
        # delete ContentRatings first
        ratings = list(self.ratings.all())
        self.ratings.clear()
        for rating in ratings:
            if rating.isOrphaned():
                rating.delete_relatives()
                rating.delete_with_dependencies()

        # delete WordFeatures before Words and Categories
        word_features = list(self.word_features.filter(default=False))
        self.word_features.clear()
        for word_feature in word_features:
            if word_feature.isOrphaned() and word_feature.isCustom():
                word_feature.delete()

        categories = list(self.categories.filter(default=False))
        self.categories.clear()
        for category in categories:
            if category.isOrphaned() and category.isCustom():
                category.delete()

        words = list(self.words.filter(default=False))
        self.words.clear()
        for word in words:
            if word.isOrphaned() and word.isCustom():
                word.delete()

    class Meta:
        default_manager_name = 'user_storage'
