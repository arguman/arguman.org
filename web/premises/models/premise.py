from markdown2 import markdown
from django.db import models
from django.conf import settings
from django.core import validators
from django.utils.html import escape
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from newsfeed import NEWS_TYPE_PREMISE
from ..mixins import DeletePreventionMixin
from ..managers import DeletePreventionManager
from . import Contention
from . import OBJECTION, SUPPORT, SITUATION
from . import MAX_PREMISE_CONTENT_LENGTH, PREMISE_TYPES, FALLACY_TYPES


class Premise(DeletePreventionMixin, models.Model):
    argument = models.ForeignKey(Contention, related_name="premises")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    parent = models.ForeignKey("self", related_name="children",
                               null=True, blank=True,
                               verbose_name=_("Parent"),
                               help_text=_("The parent of premise. If you don't choose " +
                                           "anything, it will be a main premise."))
    premise_type = models.IntegerField(
        default=SUPPORT,
        choices=PREMISE_TYPES, verbose_name=_("Premise Type"),
        help_text=render_to_string("premises/examples/premise_type.html"))
    text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Premise Content"),
        help_text=render_to_string("premises/examples/premise.html"),
        validators=[validators.MaxLengthValidator(MAX_PREMISE_CONTENT_LENGTH)])
    sources = models.TextField(
        null=True, blank=True, verbose_name=_("Sources"),
        help_text=render_to_string("premises/examples/premise_source.html"))
    is_approved = models.BooleanField(default=True, verbose_name=_("Published"))
    collapsed = models.BooleanField(default=False)
    supporters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name="supporting")
    sibling_count = models.IntegerField(default=1)  # denormalized field
    child_count = models.IntegerField(default=1)  # denormalized field
    max_sibling_count = models.IntegerField(default=1)  # denormalized field
    date_creation = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)

    objects = DeletePreventionManager()

    def __unicode__(self):
        return smart_unicode(self.text)

    def serialize(self, premise_lookup):
        return {
            'id': self.id,
            'children': [
                premise.serialize(premise_lookup)
                for premise in premise_lookup
                if premise.parent_id == self.id
            ],
            'recent_supporters': [
                supporter.serialize()
                for supporter in self.supporters.all()[:5]
            ],
            'supporter_count': self.supporter_count,
            'user': self.user.serialize(),
            'premise_type': self.premise_type,
            'premise_type_label': self.get_premise_type_display(),
            'premise_class': self.premise_class(),
            'text': self.text,
            'formatted_text': self.formatted_text,
            'sources': self.sources,
            'is_approved': self.is_approved,
            'collapsed': self.collapsed,
            'max_sibling_count': self.max_sibling_count,
            'sibling_count': self.sibling_count,
            'child_count': self.child_count,
            'date_creation': self.date_creation,
            'fallacies': self.fallacies,
            'fallacy_count': self.report_count
        }

    @models.permalink
    def get_absolute_url(self):
        return 'premise_detail', [self.argument.slug, self.pk]

    @property
    def parent_users(self):
        current = self
        parent_users_ = []
        while current.parent:
            if current.parent.user != self.user:
                parent_users_.append(current.parent.user)
            current = current.parent
        return list(set(parent_users_))


    def update_sibling_counts(self):
        count = self.get_siblings().count()
        self.get_siblings().update(sibling_count=count)

    def get_siblings(self):
        return Premise.objects.filter(parent=self.parent,
                                      argument=self.argument)

    def published_children(self):
        return self.children.filter(is_approved=True)

    def premise_class(self):
        return {
            OBJECTION: "but",
            SUPPORT: "because",
            SITUATION: "however"
        }.get(self.premise_type)

    def reported_by(self, user):
        return self.reports.filter(reporter=user).exists()

    def formatted_sources(self):
        return markdown(escape(self.sources), safe_mode=True)

    def formatted_text(self):
        return markdown(escape(self.text), safe_mode=True)

    def width(self):
        return self.published_children().count()

    def fallacies(self):
        fallacies = set(report.fallacy_type
                        for report in self.reports.all())
        mapping = dict(FALLACY_TYPES)
        return [(mapping.get(fallacy) or fallacy)
                for fallacy in fallacies]

    def get_actor(self):
        # Encapsulated for newsfeed app.
        return self.user

    def get_newsfeed_type(self):
        return NEWS_TYPE_PREMISE

    def get_newsfeed_bundle(self):
        return {
            "premise_type": self.premise_type,
            "premise_class": self.premise_class(),
            "text": self.text,
            "sources": self.sources,
            "contention": self.argument.get_newsfeed_bundle()
        }

    def get_parent(self):
        return self.parent or self.argument

    def recent_supporters(self):
        return self.supporters.values("id", "username")[0:5]

    def children_by_premise_type(self, premise_type=None):
        return self.published_children().filter(premise_type=premise_type)

    because = curry(children_by_premise_type, premise_type=SUPPORT)
    but = curry(children_by_premise_type, premise_type=OBJECTION)
    however = curry(children_by_premise_type, premise_type=SITUATION)
