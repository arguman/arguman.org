from django.db import models
from django.utils.encoding import smart_unicode

class Channel(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return smart_unicode(self.title)
