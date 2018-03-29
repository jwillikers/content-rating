from django.db import models
from django.db.models import Prefetch


class Category(models.Model):
    category = models.CharField(unique=True, max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return 'category: {}, weight: {}'.format(self.category, self.weight)

    def __repr__(self):
        return self.category

    def _dict(self):
        return {self.category: self.weight}


class WordCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    strength = models.BooleanField(
        choices=[(True, 'strong'),
                 (False, 'weak')],
        default=False)
    weight = models.SmallIntegerField(
        choices=[(0, 'innocuous'),
                 (1, 'slight'),
                 (2, 'moderate'),
                 (3, 'heavy')])

    def __str__(self):
        return 'category: {}, strength: {}, weight: {}'.format(
            self.category.category,
            self.get_strength_display(),
            self.get_weight_display())

    def __repr__(self):
        return '{} {} {}'.format(
            self.category.category,
            self.strength,
            self.weight)

    def _dict(self):
        return {'category': self.category.category,
                'strength': {self.get_strength_display(): self.strength)
                'weight': {self.get_weight_display(): self.weight)}

    def get_category(self):
        return self.category.category


class Word(models.Model):
    word_category_set = models.ManyToManyField(WordCategory)
    word = models.CharField(unique=True, max_length=30)

    def __str__(self):
        string = ''
        for word_category in self.word_category_set:
            string += word_category.__str__() + '\n'
        return string

    def __repr__(self):
        return self.word

    def _dict(self):
        return {self.word: self.get_word_categories}

    def get_word_categories():
        word_categories_dict = dict()
        for word_category in self.word_category_set:
            word_categories_dict.update(word_category._dict())
        return word_categories_dict

    def get_categories(self):
        cats = list()
        for word_category in self.word_category_set:
            cats.append(word_category.get_category())
        return cats


def get_words_of_category(category):
    if category:
        words = Word.objects.filter(word_category_set__category=category)
    else:
        words = Word.objects.all()
    return words


def get_words_of_category_strong(category, strength):
    if category:
        words = Word.objects.filter(
            word_category_set__category=category,
            word_category_set__strength=strength)
    else:
        words = Word.objects.filter(word_category_set__strength=strength)
    return words


def get_word_offensiveness(word, category):
    if word.category = category:
        offensiveness = word.get_strength_display()
    else:
        offensiveness = None
    return offensiveness

class Phrase(models.Model):
    word_category_set = models.ManyToManyField(WordCategory)
    phrase = models.CharField(unique=True, max_length=100)
    word_set = models.ManyToManyField(Word)

    def __str__(self):
        return self.phrase


class WordSpelling(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    spelling = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.spelling


class PhraseSpelling(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    spelling = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.spelling
