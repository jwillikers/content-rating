from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, Manager, PositiveSmallIntegerField

class Content(Model):
    MEDIA_TYPES = [(0, 'song'),
                   (1, 'movie'),
                   (2, 'book'),
                   (3, 'website'),
                   (4, 'document')]
    title = CharField(max_length=125)
    creator = CharField(max_length=70)
    media = PositiveSmallIntegerField(choices=MEDIA_TYPES)
    content = Manager()

    def __str__(self):
        return "{} by {}".format(self.title, self.creator)

    class Meta:
        default_manager_name = 'content'
