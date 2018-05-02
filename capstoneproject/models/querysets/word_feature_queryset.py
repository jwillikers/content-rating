from django.db.models import QuerySet


class WordFeatureQuerySet(QuerySet):
    """Custom QuerySet for WordFeature model."""

    def default(self):
        """
        Filters the WordFeatureQuerySet to only include default WordFeature
        instances.
        :return: A WordFeatureQuerySet containing only default WordFeatures.
        """
        return self.filter(default=True)
