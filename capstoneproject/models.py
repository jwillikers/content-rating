from django.db import models


class Category(models.Model):
    category = models.CharField(unique=True, max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return self.category


class WordCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    strong = models.BooleanField()
    weight = models.SmallIntegerField(
        choices=[
            (0, 'innocuous'),
            (1, 'slight'),
            (2, 'moderate'),
            (3, 'heavy')
        ])

    def __str__(self):
        return self.strong


class Word(models.Model):
    word_category_set = models.ManyToManyField(WordCategory)
    word = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.word


def get_words_of_category(category):
    if category:
        return Word.objects.filter(word_category_set__category=category)
    return Word.objects.all()


def get_words_of_category_strong(category, strong):
    if category:
        return Word.objects.filter(word_category_set__category=category, word_category_set__strong=strong)
    return Word.objects.filter(word_category_set__strong=strong)


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
