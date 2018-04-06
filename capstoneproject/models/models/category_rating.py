from django.db.models import Model, ManyToManyField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from capstoneproject.models.models.category import Category
from capstoneproject.models.fields.rating_field import RatingField


class CategoryRating(Model):
    category = ForeignKey(Category, on_delete=CASCADE)
    rating = RatingField()
