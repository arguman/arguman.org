from newsfeed import NEWS_TYPE_FALLACY
from . import Premise, Contention
from . import FALLACY_TYPES

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='reports')
    premise = models.ForeignKey(Premise,
                                related_name='reports',
                                blank=True,
                                null=True)
    contention = models.ForeignKey(Contention,
                                   related_name='reports',
                                   blank=True,
                                   null=True)
    fallacy_type = models.CharField(
        _("Fallacy Type"), choices=FALLACY_TYPES, null=True, blank=False,
        max_length=255, default="Wrong Direction",
        help_text=render_to_string("premises/examples/fallacy.html"))

    def __unicode__(self):
        return smart_unicode(self.fallacy_type)

    def get_actor(self):
        """
        Encapsulated for newsfeed app.
        """
        return self.reporter

    def get_newsfeed_type(self):
        return NEWS_TYPE_FALLACY

    def get_newsfeed_bundle(self):
        return {
            "fallacy_type": self.fallacy_type,
            "premise": self.premise.get_newsfeed_bundle(),
            "contention": self.contention.get_newsfeed_bundle()
        }
