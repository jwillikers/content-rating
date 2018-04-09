from django.db.models import Model, ManyToManyField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from capstoneproject.models.models.category import Category
from capstoneproject.models.fields.rating_field import RatingField


class CategoryRating(Model):
    """
    This Model contains data related to the Category Rating
    of a text.
    """
    category = ForeignKey(Category, on_delete=CASCADE)
    rating = RatingField()

    def __str__(self):
        string = 'CategoryRating:\n'
        string += '  Category: {}  Rating: {}'.format(self.category.name, self.rating)
        return string
