from django.test import TestCase
from capstoneproject.models.fields.positive_integer_range_field \
    import PositiveIntegerRangeField


class TestPositiveIntegerRangeField(TestCase):
    def test_constructor(self):
        field = PositiveIntegerRangeField(
            min_value=1,
            max_value=2)
