from django.db import models

from premises.constants import FEATURED_CONTENT_COUNT


class ContentionManager(models.Manager):
    def featured(self):
        return self.filter(is_featured=True)[:FEATURED_CONTENT_COUNT]
