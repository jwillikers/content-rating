from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return u'Category: %s\n' \
               u'Weight  :  %d\n' % (self.category, self.weight)


class Word(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return u'Category: %s\n' \
               u'Word    : %s\n' \
               u'Weight  : %d\n' % (self.category, self.word, self.weight)


class Phrase(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    phrase = models.CharField(max_length=100)
    weight = models.IntegerField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return u'Category : %s\n' \
               u'Phrase   : %s\n' \
               u'Weight   : %d\n' \
               u'Word     : %s\n' % (self.category, self.phrase, self.weight, self.word)


class WordSpelling(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    spelling = models.CharField(max_length=30)

    def __str__(self):
        return u'Word    : %s\n' \
               u'Spelling: %s\n' % (self.word, self.spelling)


class PhraseSpelling(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    spelling = models.CharField(max_length=100)

    def __str__(self):
        return u'Phrase  : %s\n' \
               u'Spelling: %s\n' % (self.phrase, self.spelling)
