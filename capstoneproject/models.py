from django.db import models

# I was just testing some stuff out, Jordan. Feel free to make changes.

class Category(models.Model):
    category = models.CharField(max_length=30)
    weight = models.IntegerField()
    
class Word(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    weight = models.IntegerField()