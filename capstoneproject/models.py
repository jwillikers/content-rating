from django.db import models


class Category(models.Model):
    category = models.CharField(unique=True, max_length=30)
    parent_set = models.ManyToManyField('self')
    weight = models.IntegerField()

    def __str__(self):
        return self.category


class CategoryStrong(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    strong = models.BooleanField()

    def __str__(self):
        return self.strong


class Word(models.Model):
    category_strong_set = models.ManyToManyField(CategoryStrong)
    word = models.CharField(unique=True, max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return self.word


class Phrase(models.Model):
    category_strong = models.ManyToManyField(CategoryStrong)
    phrase = models.CharField(unique=True, max_length=100)
    weight = models.IntegerField()
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
