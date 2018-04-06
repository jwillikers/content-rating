from capstoneproject.models.fields.positive_small_integer_range_field import PositiveSmallIntegerRangeField


class RatingField(PositiveSmallIntegerRangeField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        PositiveSmallIntegerRangeField.__init__(
            self, min_value=0, max_value=10, verbose_name=verbose_name,
            name=name, **kwargs)
