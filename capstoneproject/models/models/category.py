from django.db.models import ManyToManyField, CharField, Manager, \
    BooleanField, Model
from django.contrib.auth.models import User
from capstoneproject.models.fields.weight_field import WeightField


class Category(Model):
    """
    The Category class is a table that stores the offensive category and weight
    associated with an offensive word.
    """
    default = BooleanField(default=False)
    name = CharField(unique=True, max_length=30)
    weight = WeightField()
    categories = Manager()

    def __str__(self):
        """
        Overwrites the __str__ function and returns a string containing the
        category name and the weight.
        :return: A string containing the category name and the weight.
        """
        return 'Category:\n  Name: {}  Weight: {}'.format(
            self.name, self.weight)

    def __repr__(self):
        """
        Overwrites the __repr__ function and returns the name of the category.
        :return: The category name.
        """
        return self.name

    def _dict(self):
        """
        Provides a dictionary value of the category, mapping the category name
        to the weight.
        :return: A dictionary value containing the category name and weight.
        """
        return {self.name: self.weight}

    class Meta:
        default_manager_name = 'categories'