from datetime import datetime
from django.db import models
from django.db.models import signals


class DeletePreventionMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None):
        # prepare
        signals.pre_delete.send(
            sender=self.__class__,
            instance=self
        )
        # mark as deleted
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save(using=using)
        # trigger
        signals.post_delete.send(
            sender=self.__class__,
            instance=self
        )