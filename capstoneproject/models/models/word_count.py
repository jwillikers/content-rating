from django.db.models import Model, ForeignKey, CASCADE
from capstoneproject.models.models.word import Word
from capstoneproject.models.fields.word_count_field import WordCountField


class WordCount(Model):
    """
    This Model contains information regarding the number of times
    a word appears in a text.
    """
    word = ForeignKey(Word, related_name='word_counts', on_delete=CASCADE)
    count = WordCountField(default=1)

    def isRelated(self):
        return len(self.content_ratings.all()) > 0

    def isOrphaned(self):
        return len(self.content_ratings.all()) == 0

    def __str__(self):
        return "WordCount  {} - {}".format(self.word, self.count)
