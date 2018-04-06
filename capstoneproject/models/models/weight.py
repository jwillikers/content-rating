from django.db.models import Model, PositiveSmallIntegerField


class Weight(Model):
    """
    The Weight class is a table that stores the offensiveness levels associated
    with offensive words in specific
    categories.
    """
    WEIGHTS = [(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')]
    weight = PositiveSmallIntegerField(choices=WEIGHTS)

    class Meta:
        abstract = True
