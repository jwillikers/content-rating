from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, Manager, \
    PositiveSmallIntegerField


class Content(Model):
    """
    This Model contains data to identify rated content.
    """
    MEDIA_TYPES = [(0, 'song'),
                   (1, 'movie'),
                   (2, 'book'),
                   (3, 'website'),
                   (4, 'document')]
    title = CharField(max_length=125)
    creator = CharField(max_length=70)
    media = PositiveSmallIntegerField(
        choices=MEDIA_TYPES, null=True, blank=True)
    content = Manager()

    def isRelated(self):
        return len(self.content_ratings.all()) > 0

    def isOrphaned(self):
        return len(self.content_ratings.all()) == 0

    def __str__(self):
        """
        This method overwrites the __str__ function and
        returns a string containing information about the Content.
        :return: A string, containing information about the Content.
        """
        return "Media Types {}  -  {} by {}".format(
            self.media, self.title, self.creator)

    class Meta:
        default_manager_name = 'content'
