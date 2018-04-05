from capstoneproject.models.fields.positive_integer_range_field import PositiveIntegerRangeField


class WordCountField(PositiveIntegerRangeField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        PositiveIntegerRangeField.__init__(
            self, min_value=1, max_value=None, verbose_name=verbose_name,
            name=name, **kwargs)
