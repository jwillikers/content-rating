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
    strength = models.BooleanField(choices=[(True, 'strong'), (False, 'weak')], default=False)
    weight = models.SmallIntegerField(
        choices=[
            (0, 'innocuous'),
            (1, 'slight'),
            (2, 'moderate'),
            (3, 'heavy')
        ])

    def __str__(self):
        return 'category: {}, strength: {}, weight: {}'.format(self.category.category, self.get_strength_display(), self.get_weight_display())

    def __repr__(self):
        return '{} {} {}'.format(self.category.category, self.strength, self.weight)

    def _dict(self):
        return {
            'category': self.category.category,
            'strength': self.get_strength_display(),
            'weight': (self.weight, self.get_weight_display())
        }


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
        word_categories_dict = dict()
        for word_category in self.word_category_set:
            word_categories_dict.update(word_category._dict())
        return {self.word: word_categories_dict}


def get_words():
    return Word.objects.prefetch_related(Prefetch('word_category_set__category', to_attr='words_cache'))

def get_words_of_category(category):
    if category:
        return Word.objects.filter(word_category_set__category=category)
    return Word.objects.all()


def get_words_of_category_strong(category, strength):
    if category:
        return Word.objects.filter(word_category_set__category=category, word_category_set__strength=strength)
    return Word.objects.filter(word_category_set__strength=strength)


def get_word_offensiveness(word, category):
    if Word.objects.get(word=word, word_category_set__category=category.id, word_category_set__strong=True):
        return 'STRONG'
    elif Word.objects.get(word=word, word_category_set__category=category.id, word_category_set__strong=False):
        return 'WEAK'
    else:
        return 'NOT'


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
