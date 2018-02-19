from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return u'%s %d' % (self.category, self.weight)


class Word(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return u'%s %s %d' % (self.category, self.word, self.weight)


class Spelling(models.Model):
    word_or_phrase = models.ForeignKey(Word, on_delete=models.CASCADE)
    spelling = models.CharField(max_length=30)

    def __str__(self):
        return u'Word or phrase: %s \nSpelling: %s' % (self.word_or_phrase, self.spelling)


class Phrase(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    phrase = models.CharField(max_length=100)
    weight = models.IntegerField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s %s' % (self.id, self.spelling)
