from django.db.models import signals
from django.db import models
from datetime import datetime


class FormRenderer(object):
    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <div class="helptext">%s</div>',
            errors_on_separate_row=True)


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
