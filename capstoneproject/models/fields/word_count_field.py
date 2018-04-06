from capstoneproject.models.fields.positive_integer_range_field \
    import PositiveIntegerRangeField


class WordCountField(PositiveIntegerRangeField):
    def __init__(self, **kwargs):
        PositiveIntegerRangeField.__init__(
            self, min_value=1, max_value=None, **kwargs)
