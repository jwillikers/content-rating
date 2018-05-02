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
        """
        Determines if any relatives rely on this model instance.
        :return: True if relatives rely on this model instance.
        """
        return len(self.content_ratings.all()) > 0

    def isOrphaned(self):
        """
        Determines if no relatives rely on this model instance.
        :return: True if no relatives rely on this model instance.
        """
        return len(self.content_ratings.all()) == 0

    def __str__(self):
        string = 'CategoryRating:\n'
        string += '  Category: {}  Rating: {}'.format(
            self.category.name, self.rating)
        return string

    class Meta:
        """Settings for the CategoryRating model."""
        default_manager_name = 'category_ratings'
