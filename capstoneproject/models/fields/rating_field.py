from capstoneproject.models.fields.positive_small_integer_range_field \
    import PositiveSmallIntegerRangeField


class RatingField(PositiveSmallIntegerRangeField):
    """Represents a rating for Content."""

    def __init__(self, **kwargs):
        """
        Constructor for the Field.
        :param **kwargs: arguments for the constructor.
        :return:
        """
        PositiveSmallIntegerRangeField.__init__(
            self, min_value=0, max_value=10, **kwargs)
