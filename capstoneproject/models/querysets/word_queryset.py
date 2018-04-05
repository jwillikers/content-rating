from django.db.models import QuerySet, Prefetch
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word_feature import WordFeature


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
        from capstoneproject.models.models.word import Word
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
        from capstoneproject.models.models.word import Word
        if isinstance(word, str):
            word = self.filter(name=word).first()
        elif isinstance(word, int):
            word = self.filter(id=word).first()
        elif isinstance(word, Word):
            word = self.filter(id=word.id).first()
        else:
            raise TypeError('''{} is not a valid type for word'''.format(word))
        return word
