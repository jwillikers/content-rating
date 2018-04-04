"""
This file contains the Models that represent tables in the system's database and helper functions to interact with
the tables.
"""
from django.db.models import Manager, Model, CharField, IntegerField, \
    BooleanField, ForeignKey, SmallIntegerField, CASCADE, QuerySet, \
    ManyToManyField, Prefetch


class Weight(Model):
    """
    The Weight class is a table that stores the offensiveness levels associated with offensive words in specific
    categories.
    """
    WEIGHTS = [(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')]
    weight = SmallIntegerField(choices=WEIGHTS)

    class Meta:
        abstract = True


class Category(Weight):
    """
    The Category class is a table that stores the offensive category and weight associated with an offensive word.
    """
    name = CharField(unique=True, max_length=30)
    categories = Manager()

    def __str__(self):
        """
        Overwrites the __str__ function and returns a string containing the category name and the weight.
        :return: A string containing the category name and the weight.
        """
        return 'category: {}, weight: {}'.format(self.name, self.weight)

    def __repr__(self):
        """
        Overwrites the __repr__ function and returns the name of the category.
        :return: The category name.
        """
        return self.name

    def _dict(self):
        """
        Provides a dictionary value of the category, mapping the category name to the weight.
        :return: A dictionary value containing the category name and weight.
        """
        return {self.name: self.weight}

    class Meta:
        default_manager_name = 'categories'


class WordFeatureQuerySet(QuerySet):
    """
    This class represents a query set of Word Features.
    """
    def category(self, category):
        """
        Filters word features based on the given category.
        :param category: name, id, or Category representing the category.
        :return: Word features belonging to the given category.
        """
        if isinstance(category, str):
            features = self.filter(category__name=category)
        elif isinstance(category, int):
            features = self.filter(category=category)
        elif isinstance(category, Category):
            features = self.filter(category=category.id)
        else:
            raise TypeError('''{} is not a Category object, id, or name.
                '''.format(category))
        return features

    def word(self, word):
        """
        Filters word features based on the given word.
        :param word: name, id, or Word representing the word.
        :return: the word features for the given word.
        """
        if isinstance(word, str):
            features = self.filter(word_set=word)
        elif isinstance(word, int):
            features = self.filter(word_set_id=word)
        elif isinstance(word, Word):
            features = self.filter(word_set_id=word.id)
        else:
            raise TypeError('''{} is not a valid type for word'''.format(word))
        return features


class WordFeature(Weight):
    """
    This class is a table containing the Word Features associated with an offensive word.
    The table contains the overall offensiveness strength (strong or weak), the offensive category, and the
    offensiveness weight of the word and category.
    """
    STRENGTHS = [(True, 'strong'), (False, 'weak')]
    category = ForeignKey(Category, on_delete=CASCADE)
    strength = BooleanField(choices=STRENGTHS, default='weak')
    word_features = Manager()

    def __str__(self):
        """
        Overwrites the __str__ function and returns a string for an entry in the table.
        :return: A string containing the category's name, the strength, and the weight.
        """
        return 'category: {}, strength: {}, weight: {}'.format(
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
        Provides a dictionary mapping the category, strength, and weight to their corresponding values.
        :return: A dictionary with the category, strength, weight, and their associated values.
        """
        dictionary = dict()
        dictionary['category'] = self.category.name
        dictionary['strength'] = {self.get_strength_display(): self.strength}
        dictionary['weight'] = {self.get_weight_display(): self.weight}
        return dictionary
        #return {'category': self.category.name,
        #        'strength': {self.get_strength_display(): self.strength},
        #        'weight': {self.get_weight_display(): self.weight}}

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
        self.feature_queryset = self.feature_queryset.select_related('category').filter(category=category)

        feature_prefetch = Prefetch('word_features', queryset=self.feature_queryset, to_attr='word_features_list')

        words = self.prefetch_related(None).filter(word_features__category=category).prefetch_related(feature_prefetch)
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

        feature_prefetch = Prefetch('word_features', queryset=self.feature_queryset, to_attr='word_features_list')

        words = self.prefetch_related(None).filter(word_features__strength=strength).prefetch_related(feature_prefetch)
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

        feature_prefetch = Prefetch('word_features', queryset=self.feature_queryset, to_attr='word_features_list')

        words = self.prefetch_related(None).filter(word_features__weight=weight).prefetch_related(feature_prefetch)
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
    word_features = ManyToManyField(WordFeature, related_name='words')
    name = CharField(unique=True, max_length=30)
    words = WordQuerySet.as_manager()

    def __str__(self):
        """
        Overwrites the __str__ function to provide a string containing the word's name.
        :return: A string containing the word's name.
        """
        return self.name

    def __repr__(self):
        """
        Overwrites the __repr__ function to provide the name and features of the word.
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
        Provides a list of the offensive categories that the word is classified as.
        :return: A list of offensive categories that the word is classified as.
        """
        cats = list()
        for word_feature in self.word_features.all():
            cats.append(word_feature.category.name)
        return cats

    class Meta:
        default_manager_name = 'words'
