from django.contrib import admin
from .models import Category, Word, Phrase, WordSpelling, PhraseSpelling

admin.site.register(Category)
admin.site.register(Word)
admin.site.register(Phrase)
admin.site.register(WordSpelling)
admin.site.register(PhraseSpelling)

