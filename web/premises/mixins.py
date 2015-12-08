from datetime import datetime

from django.db.models import signals
from django.db import models

from premises.utils import int_or_zero


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


class PaginationMixin(object):

    def get_offset(self):
        return int_or_zero(self.request.GET.get("offset"))

    def get_limit(self):
        return self.get_offset() + self.paginate_by

    def has_next_page(self):
        total = self.get_contentions(paginate=False).count()
        return total > (self.get_offset() + self.paginate_by)

    def get_next_page_url(self):
        offset = self.get_offset() + self.paginate_by
        return '?offset=%(offset)s' % {
            "offset": offset
        }


class NextURLMixin(object):
    # todo: find a proper way to handle this and remove this mixin
    def get_view_name(self):
        view = self.request.GET.get("view")
        return view if view in ["tree", "list"] else ""

    def get_next_parameter(self):
        if self.get_view_name() == "list":
            return "?view=list"
        return ""
