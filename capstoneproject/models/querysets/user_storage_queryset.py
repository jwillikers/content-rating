from django.db.models import QuerySet


class UserStorageQuerySet(QuerySet):
    """A custom QuerySet for the UserStorage model."""

    def autocreate(self, user):
        """
        Create and initialize a new UserStorage instance.
        :param user: The User that will own this UserStorage.
        :return:
        """
        from capstoneproject.models.models.category import Category
        from capstoneproject.models.models.word import Word
        from capstoneproject.models.models.word_feature import WordFeature
        from capstoneproject.models.models.user_storage import UserStorage
        user_storage = UserStorage.user_storage.create(
            id=user.id,
            user=user)
        user_storage.save()
        for category in Category.categories.default():
            user_storage.categories.add(category)
        for word in Word.words.default():
            user_storage.words.add(word)
        for word_feature in WordFeature.word_features.default():
            user_storage.word_features.add(word_feature)
