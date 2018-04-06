from django.db.models import ManyToManyField, ForeignKey, BooleanField, \
    Manager, CASCADE, Model
from django.contrib.auth.models import User
from capstoneproject.models.models.category import Category
from capstoneproject.models.fields.strength_field import StrengthField
from capstoneproject.models.fields.weight_field import WeightField


class WordFeature(Model):
    """
    This class is a table containing the Word Features associated with an
    offensive word. The table contains the overall offensiveness strength
    (strong or weak), the offensive category, and the offensiveness weight of
    the word and category.
    """
    default = BooleanField(default=False)
    category = ForeignKey(Category, on_delete=CASCADE)
    strength = StrengthField(default='strong')
    weight = WeightField()
    word_features = Manager()

    def __str__(self):
        """
        Overwrites the __str__ function and returns a string for a table entry.
        :return: A string containing the category's name, strength, and weight.
        """
        return 'Word Feature:\n  Category: {}\n  Strength: {}\n  Weight: {}'\
            .format(
                self.category.name,
                self.get_strength_display(),
                self.get_weight_display())

    def __repr__(self):
        """
        Overwrites the __repr__ function.
        :return: A triple containing the category, strength, and weight.
        """
        return '{} {} {}'.format(
            self.category,
            self.strength,
            self.weight)

    def _dict(self):
        """
        Provides a dictionary mapping the category, strength, and weight to
        their corresponding values.
        :return: A dictionary with the category, strength, weight, and
        their associated values.
        """
        dictionary = dict()
        dictionary['category'] = self.category.name
        dictionary['strength'] = {self.get_strength_display(): self.strength}
        dictionary['weight'] = {self.get_weight_display(): self.weight}
        return dictionary

    class Meta:
        default_manager_name = 'word_features'
