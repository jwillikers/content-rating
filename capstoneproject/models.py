from django.db import models


# I was just testing some stuff out, Jordan. Feel free to make changes.

class Category(models.Model):
    category = models.CharField(max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return u'%s %d' % (self.category, self.weight)

    class Meta:
        ordering = ['category']

class Word(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    weight = models.IntegerField()

    def __str__(self):
        return u'%s %d' % (self.word, self.weight)

    class Meta:
        ordering = ['word', 'category_id']

'''
class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username', 'email']
'''