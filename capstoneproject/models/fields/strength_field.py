from django.db.models import BooleanField


class StrengthField(BooleanField):
    STRENGTHS = [(True, 'strong'), (False, 'weak')]

    def __init__(self, **kwargs):
        kwargs['choices'] = StrengthField.STRENGTHS
        BooleanField.__init__(
            self, **kwargs)

    def strong(self):
        return self.value

    def weak(self):
        return not self.value
