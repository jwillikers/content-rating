from capstoneproject.models.fields.positive_small_integer_range_field \
    import PositiveSmallIntegerRangeField


class WeightField(PositiveSmallIntegerRangeField):
    """The Weight field stores the offensiveness levels associated
    with offensive words in specific
    categories."""
    WEIGHTS = [(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')]

    def __init__(self, **kwargs):
        """
        Constructor for the Field.
        :param **kwargs: arguments for the constructor.
        :return:
        """
        kwargs['choices'] = WeightField.WEIGHTS
        PositiveSmallIntegerRangeField.__init__(
            self, min_value=0, max_value=3,
            **kwargs)
