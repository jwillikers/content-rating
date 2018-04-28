from django.db.models import QuerySet


class WordFeatureQuerySet(QuerySet):
    def default(self):
        return self.filter(default=True)
