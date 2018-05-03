from django.db.models import Model, ManyToManyField, CharField, BooleanField
from django.contrib.auth.models import User
from capstoneproject.models.querysets.word_queryset import WordQuerySet
from capstoneproject.models.models.word_feature import WordFeature


class Word(Model):
    """A class representing the system's table of offensive Words."""
    default = BooleanField(default=False)
    word_features = ManyToManyField(WordFeature, related_name='words')
    name = CharField(unique=True, max_length=30)
    words = WordQuerySet.as_manager()

    def __str__(self):
        """Overwrites the __str__ function to provide a string containing the
        word's name.

        Return:
            str: The word's name.
        """
        return 'Word: {}'.format(self.name)

    def __repr__(self):
        """
        Overwrites the __repr__ function to provide the name and features of
        the word.
        :return: A string containing the word's name and word features
        """
        return 'word: {} features: {}'.format(self.name, self.word_features)

    def _dict(self):
        """
        Provides a dictionary mapping the word name to the word's features.
        :return: A dictionary containing the word's name and word's features.
        """
        return {self.name: self.get_word_features()}

    def isDefault(self):
        """
        Determines if this model instance is a default.
        :return: True if this model instance is a default.
        """
        return self.default

    def isCustom(self):
        """
        Determines if this model instance is User created.
        :return: True if this model instance is User created.
        """
        return not self.default

    def isRelated(self):
        """
        Determines if any relatives rely on this model instance.
        :return: True if relatives rely on this model instance.
        """
        return len(self.user_storage.all()) > 0 \
            or len(self.word_features.all()) > 0

    def isOrphaned(self):
        """
        Determines if no relatives rely on this model instance.
        :return: True if no relatives rely on this model instance.
        """
        return len(self.user_storage.all()) == 0 \
            and len(self.word_features.all()) == 0

    def delete_relatives(self):
        """
        Deletes this model instance's related model instances.
        :return:
        """
        word_features = list(self.word_features.all())
        for word_feature in word_features:
            if word_feature.isOrphaned() and word_feature.isCustom():
                word_feature.delete()

    def get_word_features(self):
        """
        Provides the word's features
        :return: A dictionary mapping a word to its features.
        """
        word_features_list = []
        for word_feature in self.word_features.all():
            word_features_list.append(word_feature._dict())

        return word_features_list

    def get_categories(self):
        """
        Provides a list of the offensive categories of which the word belongs.
        :return: A list of offensive categories that the word is classified as.
        """
        cats = list()
        for word_feature in self.word_features.all():
            cats.append(word_feature.category.name)
        return cats

    def delete(self, *args, **kwargs):
        """
        Deletes this model instance along with any relatives that \
        are only related to it.
        :param *args: Possible arguments to the default delete method.
        :param *kwargs: Possible arguments to the default delete method.
        :return:
        """
        self.delete_relatives()
        super().delete(*args, **kwargs)

    class Meta:
        """Settings for the Word model."""
        default_manager_name = 'words'
