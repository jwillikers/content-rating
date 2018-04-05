"""
This file contains the Models that represent tables in the system's database
and helper functions to interact with the tables.
"""
from django.contrib.auth.models import User
from django.db.models import Manager, Model, CharField, IntegerField, \
    BooleanField, ForeignKey, SmallIntegerField, \
    CASCADE, QuerySet, DateTimeField, \
    ManyToManyField, Prefetch, \
    PositiveSmallIntegerField, PositiveIntegerField


class PositiveSmallIntegerRangeField(PositiveSmallIntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None,
                 max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        PositiveSmallIntegerField.__init__(
            self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(PositiveSmallIntegerRangeField,
                     self).formfield(**defaults)


class PositiveIntegerRangeField(PositiveIntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None,
                 max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        PositiveIntegerField.__init__(
            self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(PositiveIntegerRangeField, self).formfield(**defaults)


class RatingField(PositiveSmallIntegerRangeField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        PositiveSmallIntegerRangeField.__init__(
            self, min_value=0, max_value=10, verbose_name=verbose_name,
            name=name, **kwargs)


class WordCountField(PositiveIntegerField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        PositiveIntegerRangeField.__init__(
            self, min_value=1, max_value=None, verbose_name=verbose_name,
            name=name, **kwargs)


class Weight(Model):
    """
    The Weight class is a table that stores the offensiveness levels associated
    with offensive words in specific categories.
    """
    WEIGHTS = [(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')]
    weight = PositiveSmallIntegerField(choices=WEIGHTS)

    class Meta:
        abstract = True

    def __str__(self):
        return 'Weight {}'.format(self.weight)


class CategoryQuerySet(QuerySet):
    category_queryset = None

    def user(self, user):
        if isinstance(user, str):
            user = User.objects.get(username=user)
        elif isinstance(user, int):
            user = User.objects.get(pk=user)
        elif isinstance(user, User):
            pass
        else:
            raise TypeError('''{} is not a valid type for user'''.format(user))

        category_prefetch = Prefetch(
            'user_storage__user',
            queryset=self.category_queryset,
            to_attr='users_list')

        filtered = self.prefetch_related(None).filter(
            user_storage__user=user
            ).prefetch_related(category_prefetch)
        return filtered


class Category(Weight):
    """
    The Category class is a table that stores the offensive category and weight
    associated with an offensive word.
    """
    user = ManyToManyField(User, related_name='categories', null=True, blank=True)
    name = CharField(unique=True, max_length=30)
    categories = Manager()

    def __str__(self):
        """
        Overwrites the __str__ function and returns a string containing the
        category name and the weight.
        :return: A string containing the category name and the weight.
        """
        return 'Category:\n  Name: {}  Weight: {}'.format(self.name, self.weight)

    def __repr__(self):
        """
        Overwrites the __repr__ function and returns the name of the category.
        :return: The category name.
        """
        return self.name

    def _dict(self):
        """
        Provides a dictionary value of the category, mapping the category name
        to the weight.
        :return: A dictionary value containing the category name and weight.
        """
        return {self.name: self.weight}

    class Meta:
        default_manager_name = 'categories'


class CategoryRating(Model):
    user = ManyToManyField(
        User, related_name='category_ratings', null=True, blank=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    rating = RatingField()

    def __str__(self):
        string = 'CategoryRating\n'
        string += '  User: {}\n'.format(self.user)
        string += '  Category: {}\n'.format(self.category)
        string += '  Rating: {}'.format(self.rating)


class WordFeature(Weight):
    """
    This class is a table containing the Word Features associated with an
    offensive word. The table contains the overall offensiveness strength
    (strong or weak), the offensive category, and the offensiveness weight of
    the word and category.
    """
    STRENGTHS = [(True, 'strong'), (False, 'weak')]
    user = ManyToManyField(User, related_name='word_features', null=True, blank=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    strength = BooleanField(choices=STRENGTHS, default='weak')
    word_features = Manager()

    def __str__(self):
        """
        Overwrites the __str__ function and returns a string for a table entry.
        :return: A string containing the category's name, strength, and weight.
        """
        return 'Word Feature:\n  Category: {}\n  Strength: {}\n  Weight: {}'\
            .format(
                self.category.name,
                self.get_strength_display(),
                self.get_weight_display())

    def __repr__(self):
        """
        Overwrites the __repr__ function.
        :return: A triple containing the category, strength, and weight.
        """
        return '{} {} {}'.format(
            self.category,
            self.strength,
            self.weight)

    def _dict(self):
        """
        Provides a dictionary mapping the category, strength, and weight to
        their corresponding values.
        :return: A dictionary with the category, strength, weight, and
        their associated values.
        """
        dictionary = dict()
        dictionary['category'] = self.category.name
        dictionary['strength'] = {self.get_strength_display(): self.strength}
        dictionary['weight'] = {self.get_weight_display(): self.weight}
        return dictionary

    class Meta:
        default_manager_name = 'word_features'


class WordQuerySet(QuerySet):
    """
    This class represents a QuerySet of a Word
    """
    feature_queryset = None

    def category(self, category):
        """
        Filters words based on given category.
        :param category: name, id, or Category representing the category.
        :return: A QuerySet of words belonging to the given category.
        """
        if isinstance(category, str):
            try:
                category = Category.categories.get(name=category.lower())
            except Category.DoesNotExist:
                return self.none()
        elif isinstance(category, int):
            try:
                category = Category.categories.get(pk=category)
            except Category.DoesNotExist:
                return self.none()
        elif isinstance(category, Category):
            pass
        else:
            raise TypeError('''{} is not a Category object, id, or name.
                '''.format(category))

        if not self.feature_queryset:
            self.feature_queryset = WordFeature.word_features.all()
        self.feature_queryset = self.feature_queryset.select_related(
            'category').filter(category=category)

        feature_prefetch = Prefetch(
            'word_features',
            queryset=self.feature_queryset,
            to_attr='word_features_list')

        words = self.prefetch_related(None).filter(
            word_features__category=category
            ).prefetch_related(feature_prefetch)
        return words

    def strength(self, strength):
        """
        Filters words based on the given strength.
        :param strength: string or numeric form of the strength.
        :return: A QuerySet of words containing the given strength.
        """
        if isinstance(strength, bool):
            pass
        elif isinstance(strength, str):
            strength = strength.lower()
            found = False
            for val, model_strength in WordFeature.STRENGTHS:
                if strength == model_strength:
                    strength = val
                    found = True
            if not found:
                raise ValueError('{} is not a valid strength choice'.format(
                    strength))
        else:
            raise TypeError('''{} is not a valid type for strength
                '''.format(strength))
        if self.feature_queryset is None:
            self.feature_queryset = WordFeature.word_features.all()
        self.feature_queryset = self.feature_queryset.filter(strength=strength)

        feature_prefetch = Prefetch(
            'word_features',
            queryset=self.feature_queryset,
            to_attr='word_features_list')

        words = self.prefetch_related(None).filter(
            word_features__strength=strength
            ).prefetch_related(feature_prefetch)
        return words

    def weight(self, weight):
        """
        Filters the words based on the given weight.
        :param weight: string or numeric form of the weight.
        :return: A QuerySet of words containing the given weight.
        """
        if isinstance(weight, int):
            found = False
            for val, _ in WordFeature.WEIGHTS:
                if weight == val:
                    found = True
                    break
            if not found:
                raise ValueError('''{} is not a valid weight choice between 0
                    and 3 inclusive.'''.format(weight))
        elif isinstance(weight, str):
            weight = weight.lower()
            found = False
            for val, model_weight in WordFeature.WEIGHTS:
                if weight == model_weight:
                    weight = val
                    found = True
            if not found:
                raise ValueError('''{} is not one of the 4 valid weight choices:
                    innocuous, slight, moderate, or heavy.'''.format(weight))
        else:
            raise TypeError('''{} is not a valid type for weight
                '''.format(weight))
        if self.feature_queryset is None:
            self.feature_queryset = WordFeature.word_features.all()
        self.feature_queryset = self.feature_queryset.filter(weight=weight)

        feature_prefetch = Prefetch(
            'word_features',
            queryset=self.feature_queryset,
            to_attr='word_features_list')

        words = self.prefetch_related(None).filter(
            word_features__weight=weight
            ).prefetch_related(feature_prefetch)
        return words

    def word(self, word):
        """
        Filters words based on given word.
        :param word: name, id, or Word representing the word.
        :return: A QuerySet of the word given.
        """
        if isinstance(word, str):
            word = self.filter(name=word)
        elif isinstance(word, int):
            word = self.filter(id=word)
        elif isinstance(word, Word):
            word = self.filter(id=word.id)
        else:
            raise TypeError('''{} is not a valid type for word'''.format(word))
        return word

    def get_word(self, word):
        """
        Retrieves the given word.
        :param word: name, id, or Word representing the word.
        :return: The Word given or None if not found.
        """
        if isinstance(word, str):
            word = self.filter(name=word).first()
        elif isinstance(word, int):
            word = self.filter(id=word).first()
        elif isinstance(word, Word):
            word = self.filter(id=word.id).first()
        else:
            raise TypeError('''{} is not a valid type for word'''.format(word))
        return word


class Word(Model):
    """
    A class representing the system's table of offensive Words.
    """
    user = ManyToManyField(User, related_name='words', null=True, blank=True)
    word_features = ManyToManyField(WordFeature, related_name='words')
    name = CharField(unique=True, max_length=30)
    words = WordQuerySet.as_manager()

    def __str__(self):
        """
        Overwrites the __str__ function to provide a string containing the
        word's name.
        :return: The word's name as a String.
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

    class Meta:
        default_manager_name = 'words'


class WordCount(Model):
    word = ForeignKey(Word, on_delete=CASCADE)
    count = WordCountField(default=1)

    def __str__(self):
        return "WordCount  {} - {}".format(self.word, self.count)


class Content(Model):
    MEDIA_TYPES = [(0, 'song'),
                   (1, 'movie'),
                   (2, 'book'),
                   (3, 'website'),
                   (4, 'document')]
    title = CharField(max_length=125)
    creator = CharField(max_length=70)
    media = PositiveSmallIntegerField(choices=MEDIA_TYPES)
    content = Manager()

    def __str__(self):
        return "Media Types {}  -  {} by {}".format(self.media, self.title, self.creator)

    class Meta:
        default_manager_name = 'content'


class Rating(Model):
    content = ForeignKey(Content, on_delete=CASCADE)
    rating = RatingField(default=0)
    category_ratings = ManyToManyField(
        CategoryRating,
        related_name='ratings')
    word_counts = ManyToManyField(WordCount, related_name='ratings')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    ratings = Manager()

    class Meta:
        default_manager_name = 'ratings'

    def __str__(self):
        string = 'Rating\n'
        string += '  Overall Rating: {}\n'.format(self.rating)
        string += '  Category Ratings: {}\n'.format(self.category_ratings)
        string += '  Word Counts: {}\n'.format(self.word_counts)
        string += '  Created: {}    Updated: {}\n'. format(self.created, self.updated)
        return string


class UserStorage(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    ratings = ManyToManyField(
        Rating, related_name='user_storage',
        null=True, blank=True)
    word_features = ManyToManyField(
        WordFeature, related_name='user_storage',
        null=True, blank=True)
    categories = ManyToManyField(
        Category, related_name='user_storage', null=True, blank=True)
    user_storage = Manager()

    class Meta:
        default_manager_name = 'user_storage'

    def __str__(self):
        string = 'User Storage:\n'
        string += '  User: {}\n'.format(self.user.username)
        string += '  Ratings: {}\n'.format(self.ratings)
        string += '  Word Features: {}\n'.format(self.word_features)
        string += '  Categories: {}\n'.format(self.categories)
        return string
