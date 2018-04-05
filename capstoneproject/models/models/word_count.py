from django.db.models import Model, ForeignKey, CASCADE
from capstoneproject.models.models.word import Word
from capstoneproject.models.fields.word_count_field import WordCountField


class WordCount(Model):
    word = ForeignKey(Word, on_delete=CASCADE)
    count = WordCountField(default=1)
