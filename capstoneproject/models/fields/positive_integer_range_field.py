from django.db.models import PositiveIntegerField


class PositiveIntegerRangeField(PositiveIntegerField):
    """Field for Integers in a specific, positive range."""

    def __init__(
            self,
            min_value=None,
            max_value=None,
            **kwargs):
        """
        Constructor for the Field.
        :param min_value: The minimum acceptable value for the field.
        :param max_value: The maximum acceptable value for the field.
        :param **kwargs: Arguments supplied for the constructor.
        :return:
        """
        self.min_value, self.max_value = min_value, max_value
        PositiveIntegerField.__init__(
            self, **kwargs)

    def formfield(self, **kwargs):
        """
        Sanitizes User inputted field.
        :param **kwargs: arguments supplied for the constructor.
        :return: the result of PositiveIntegerField's formfield.
        """
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(PositiveIntegerRangeField, self).formfield(**defaults)
