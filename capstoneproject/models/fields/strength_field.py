from django.db.models import BooleanField


class StrengthField(BooleanField):
    """Represents a WordFeature's strength for a Category."""
    STRENGTHS = [(True, 'strong'), (False, 'weak')]

    def __init__(self, **kwargs):
        """
        Constructor for the Field.
        :param **kwargs: arguments for the constructor.
        :return:
        """
        kwargs['choices'] = StrengthField.STRENGTHS
        BooleanField.__init__(
            self, **kwargs)

    def strong(self):
        """
        Determines whether the Strength field is strong or not.
        :return: True if the Strength field is strong
        """
        return self.value

    def weak(self):
        """
        Determines whether the Strength field is weak or not.
        :return: True if the Strength field is strong
        """
        return not self.value
