from django.db.models import PositiveSmallIntegerField


class PositiveSmallIntegerRangeField(PositiveSmallIntegerField):
    """Field for Small Integers in a specific, positive range.

    This class was based off of <a href="
    https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
    ">this stackoverflow answer</a> by NathanD.
    """

    def __init__(self, min_value=None,
                 max_value=None, **kwargs):
        """Constuctor for the Field.

        :param min_value: The minimum acceptable value for the field.
        :param max_value: The maximum acceptable value for the field.
        :param **kwargs: Arguments supplied for the constructor.
        :return:
        """
        self.min_value, self.max_value = min_value, max_value
        PositiveSmallIntegerField.__init__(
            self, **kwargs)

    def formfield(self, **kwargs):
        """Sanitizes User inputted field.

        :param kwargs: arguments supplied for the constructor.
        :return: the result of PositiveSmallIntegerField's formfield
        """
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(PositiveSmallIntegerRangeField,
                     self).formfield(**defaults)
