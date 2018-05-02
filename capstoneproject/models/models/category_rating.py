from django.db.models \
    import Model, ManyToManyField, ForeignKey, CASCADE, Manager
from django.contrib.auth.models import User


class CategoryRating(Model):
    """
    This Model contains data related to the Category Rating
    of a text.
    """
    from capstoneproject.models.models.category import Category
    from capstoneproject.models.fields.rating_field import RatingField
    category = ForeignKey('Category', related_name='category_ratings',
                          on_delete=CASCADE)
    rating = RatingField()
    category_ratings = Manager()

    def isRelated(self):
        return len(self.content_ratings.all()) > 0

    def isOrphaned(self):
        return len(self.content_ratings.all()) == 0

    def __str__(self):
        string = 'CategoryRating:\n'
        string += '  Category: {}  Rating: {}'.format(
            self.category.name, self.rating)
        return string

    class Meta:
        default_manager_name = 'category_ratings'
