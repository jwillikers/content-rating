from django.db import models
from django.db.models import Manager, Model, CharField, IntegerField, \
    BooleanField, ForeignKey, SmallIntegerField, CASCADE, QuerySet, \
    ManyToManyField


class Weight(Model):
    WEIGHTS = [(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')]
    weight = SmallIntegerField(choices=WEIGHTS)

    class Meta:
        abstract = True


class Category(Weight):
    name = CharField(unique=True, max_length=30)
    categories = Manager()

    def __str__(self):
        return 'category: {}, weight: {}'.format(self.name, self.weight)

    def __repr__(self):
        return self.name

    def _dict(self):
        return {self.name: self.weight}

    class Meta:
        default_manager_name = 'categories'


class WordFeature(Weight):
    STRENGTHS = [(True, 'strong'), (False, 'weak')]
    category = ForeignKey(Category, on_delete=CASCADE)
    strength = BooleanField(choices=STRENGTHS, default='weak')
    word_features = Manager()

    def __str__(self):
        return 'category: {}, strength: {}, weight: {}'.format(
            self.category.name,
            self.get_strength_display(),
            self.get_weight_display())

    def __repr__(self):
        return '{} {} {}'.format(
            self.category.name,
            self.strength,
            self.weight)

    def _dict(self):
        return {'category': self.category.name,
                'strength': {self.get_strength_display(): self.strength},
                'weight': {self.get_weight_display(): self.weight}}

    class Meta:
        default_manager_name = 'word_features'


class WordQuerySet(QuerySet):
    def category(self, category):
        """Filters words based on given category.

        Args:
            category: name, id, or Category representing the category.

        Returns:
            QuerySet: Words belonging to the given category.
        """
        if isinstance(category, str):
            words = self.filter(word_features__category__name=category)
        elif isinstance(category, int):
            words = self.filter(word_features__category=category)
        elif isinstance(category, Category):
            words = self.filter(word_features__category=category.id)
        else:
            raise TypeError()
        return words

    def strength(self, strength):
        """Filters words based on the given strength.

        Args:
            strength: string or numeric form of the strength.

        Returns:
            QuerySet: Words containing the given strength.
        """
        if isinstance(strength, bool):
            word_features = self.filter(word_features__strength=strength)
        elif isinstance(strength, str):
            strength = strength.lower()
            found = False
            for val, model_strength in WordFeature.STRENGTHS:
                if strength == model_strength:
                    word_features = self.filter(
                        word_features__strength=val)
                    found = True
            if not found:
                raise TypeError()
        else:
            raise TypeError()
        return word_features

    def weight(self, weight):
        """Filters words based on the given weight.

        Args:
            weight: string or numeric form of the weight.

        Returns:
            QuerySet: Words containing the given weight.
        """
        if isinstance(weight, int):
            found = False
            for val, _ in WordFeature.WEIGHTS:
                if weight == val:
                    word_features = self.filter(word_features__weight=weight)
                    found = True
                    break
            if not found:
                raise TypeError()
        elif isinstance(strength, str):
            weight = weight.lower()
            found = False
            for val, model_weight in WordFeature.WEIGHTS:
                if weight == model_weight:
                    word_features = self.filter(
                        word_features__weight=val)
                    found = True
            if not found:
                raise TypeError()
        else:
            raise TypeError()
        return word_features

    def word(self, word):
        """Filters words based on given word.

        Args:
            word: name, id, or Word representing the word.

        Returns:
            QuerySet: the word given.
        """
        if isinstance(word, str):
            word = self.filter(name=word)
        elif isinstance(word, int):
            word = self.filter(id=word)
        elif isinstance(word, Word):
            word = self.filter(id=word.id)
        else:
            raise TypeError()
        return word

    def get_word(self, word):
        """Retrieves the given word.

        Args:
            word: name, id, or Word representing the word.

        Returns:
            Word: the word given or None if not found.
        """
        if isinstance(word, str):
            word = self.filter(name=word).first()
        elif isinstance(word, int):
            word = self.filter(id=word).first()
        elif isinstance(word, Word):
            word = self.filter(id=word.id).first()
        else:
            word = None
        return word


class Word(Model):
    word_features = ManyToManyField(WordFeature)
    name = CharField(unique=True, max_length=30)
    words = WordQuerySet.as_manager()

    def __str__(self):
        string = self.name + '\n'
        for word_feature in self.word_features.all():
            string += '\t' + word_feature.__str__() + '\n'
        return string

    def __repr__(self):
        return self.name

    def _dict(self):
        return {self.name: self.get_word_features()}

    def get_word_features(self):
        word_features_dict = dict()
        for word_feature in self.word_features:
            word_features_dict.update(word_feature._dict())
        return word_features_dict

    def get_categories(self):
        cats = list()
        for word_feature in self.word_features:
            cats.append(word_feature.get_category())
        return cats

    class Meta:
        default_manager_name = 'words'
