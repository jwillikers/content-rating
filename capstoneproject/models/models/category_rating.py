from django.db.models import Model, ManyToManyField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from capstoneproject.models.models.category import Category
from capstoneproject.models.fields.rating_field import RatingField


class CategoryRating(Model):
    user = ManyToManyField(
        User, related_name='category_ratings', blank=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    rating = RatingField()
