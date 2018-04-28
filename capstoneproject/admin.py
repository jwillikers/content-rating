from django.contrib import admin
from capstoneproject.models.models.category import Category
from capstoneproject.models.models.word_feature import WordFeature
from capstoneproject.models.models.word import Word

admin.site.register(Category)
admin.site.register(Word)
admin.site.register(WordFeature)
