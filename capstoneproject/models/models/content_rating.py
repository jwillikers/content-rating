from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, ManyToManyField, DateTimeField, Manager, CASCADE
from capstoneproject.models.models.content import Content
from capstoneproject.models.models.category_rating import CategoryRating
from capstoneproject.models.models.word_count import WordCount
from capstoneproject.models.fields.rating_field import RatingField


class ContentRating(Model):
    content = ForeignKey(Content, on_delete=CASCADE)
    rating = RatingField(default=0)
    category_ratings = ManyToManyField(
        CategoryRating,
        related_name='content_ratings')
    word_counts = ManyToManyField(WordCount, related_name='content_ratings')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    content_ratings = Manager()

    class Meta:
        default_manager_name = 'content_ratings'
