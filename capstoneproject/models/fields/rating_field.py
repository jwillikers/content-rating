from capstoneproject.models.fields.positive_small_integer_range_field \
    import PositiveSmallIntegerRangeField


class RatingField(PositiveSmallIntegerRangeField):
    def __init__(self, **kwargs):
        PositiveSmallIntegerRangeField.__init__(
            self, min_value=0, max_value=10, **kwargs)
