from django.contrib import admin
from .models import Category, Word, WordFeature

admin.site.register(Category)
admin.site.register(Word)
admin.site.register(WordFeature)
