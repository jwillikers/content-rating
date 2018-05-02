from capstoneproject.models.fields.positive_integer_range_field \
    import PositiveIntegerRangeField


class WordCountField(PositiveIntegerRangeField):
    """Stores counts of a specific Word."""

    def __init__(self, **kwargs):
        """
        Constructor for the Field.
        :param **kwargs: arguments for the constructor.
        :return:
        """
        PositiveIntegerRangeField.__init__(
            self, min_value=1, max_value=None, **kwargs)
