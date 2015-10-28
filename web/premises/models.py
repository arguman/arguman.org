# -*- coding: utf-8 -*-
import json
import operator
from django.utils import timezone
import os
from datetime import datetime, timedelta
from math import log


from uuid import uuid4
from django.utils.html import escape
from markdown2 import markdown
from unidecode import unidecode

from django.core import validators
from django.conf import settings
from django.template.loader import render_to_string
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from newsfeed.constants import (
    NEWS_TYPE_FALLACY, NEWS_TYPE_PREMISE, NEWS_TYPE_CONTENTION)
from premises.constants import MAX_PREMISE_CONTENT_LENGTH
from premises.managers import ContentionManager, DeletePreventionManager
from premises.mixins import DeletePreventionMixin


OBJECTION = 0
SUPPORT = 1
SITUATION = 2

epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)

PREMISE_TYPES = (
    (OBJECTION, _("but")),
    (SUPPORT, _("because")),
    (SITUATION, _("however")),
)

FALLACY_TYPES = (
    ("BeggingTheQuestion,", _("Begging The Question")),
    ("IrrelevantConclusion", _("Irrelevant Conclusion")),
    ("FallacyOfIrrelevantPurpose", _("Fallacy Of Irrelevant Purpose")),
    ("FallacyOfRedHerring", _("Fallacy Of Red Herring")),
    ("ArgumentAgainstTheMan", _("Argument Against TheMan")),
    ("PoisoningTheWell", _("Poisoning The Well")),
    ("FallacyOfTheBeard", _("Fallacy Of The Beard")),
    ("FallacyOfSlipperySlope", _("Fallacy Of Slippery Slope")),
    ("FallacyOfFalseCause", _("Fallacy Of False Cause")),
    ("FallacyOfPreviousThis", _("Fallacy Of Previous This")),
    ("JointEffect", _("Joint Effect")),
    ("WrongDirection", _("Wrong Direction")),
    ("FalseAnalogy", _("False Analogy")),
    ("SlothfulInduction", _("Slothful Induction")),
    ("AppealToBelief", _("Appeal To Belief")),
    ("PragmaticFallacy", _("Pragmatic Fallacy")),
    ("FallacyOfIsToOught", _("Fallacy Of Is To Ought")),
    ("ArgumentFromForce", _("Argument From Force")),
    ("ArgumentToPity", _("Argument To Pity")),
    ("PrejudicialLanguage", _("Prejudicial Language")),
    ("FallacyOfSpecialPleading", _("Fallacy Of Special Pleading")),
    ("AppealToAuthority", _("Appeal To Authority"))
)


class Channel(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return smart_unicode(self.title)


class Contention(DeletePreventionMixin, models.Model):
    channel = models.ForeignKey(Channel, related_name='contentions',
                                null=True, blank=True)
    title = models.CharField(
        max_length=255, verbose_name=_("Argument"),
        help_text=render_to_string("premises/examples/contention.html"))
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(
        null=True, blank=True, verbose_name=_("Description"), )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    owner = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Original Discourse"),
        help_text=render_to_string("premises/examples/owner.html"))
    sources = models.TextField(
        null=True, blank=True,
        verbose_name=_("Sources"),
        help_text=render_to_string("premises/examples/sources.html"))
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=5, null=True)

    score = models.FloatField(blank=True, null=True)
    objects = ContentionManager()

    class Meta:
        ordering = ["-date_creation"]

    def __unicode__(self):
        return smart_unicode(self.title)

    def serialize(self, authenticted_user=None):
        premises = (self.premises
                    .filter(is_approved=True)
                    .select_related('user')
                    .prefetch_related('supporters', 'reports')
                    .annotate(
                        report_count=Count('reports'),
                        supporter_count=Count('supporters', distinct=True)
                    ))
        
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'title': self.title,
            'description': self.description,
            'owner': self.owner,
            'sources': self.sources,
            'is_published': self.is_published,
            'slug': self.slug,
            'absolute_url': self.get_absolute_url(),
            'language': self.language,
            'full_url': self.get_full_url(),
            'premises': [premise.serialize(premises, authenticted_user) 
                         for premise in premises
                         if premise.parent_id is None],
            'date_creation': self.date_creation
        }

    @models.permalink
    def get_absolute_url(self):
        return 'contention_detail', [self.slug]

    def epoch_seconds(self, date):
        """Returns the number of seconds from the epoch to date."""
        td = date - epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    def calculate_score(self):
        """The hot formula. Should match the equivalent function in postgres."""
        s = self.premises.exclude(user__id=self.user.id).count()
        if s < 1:
            return 0
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = self.epoch_seconds(self.date_creation) - 1134028003
        return round(sign * order + seconds / 45000, 7)

    def get_full_url(self):
        return "http://%(language)s.%(domain)s%(path)s" % {
            "language": self.language,
            "domain": settings.BASE_DOMAIN,
            "path": self.get_absolute_url()
        }

    def save(self, *args, **kwargs):
        """
        - Make unique slug if it is not given.
        """
        if not self.slug:
            slug = slugify(unidecode(self.title))
            duplications = Contention.objects.filter(slug=slug)
            if duplications.exists():
                self.slug = "%s-%s" % (slug, uuid4().hex)
            else:
                self.slug = slug

        if not kwargs.pop('skip_date_update', False):
            self.date_modification = datetime.datetime.now()
        return super(Contention, self).save(*args, **kwargs)

    def published_premises(self, parent=None, ignore_parent=False):
        premises = self.premises.filter(is_approved=True)
        if ignore_parent:
            return premises
        return premises.filter(parent=parent)

    published_children = published_premises

    def children_by_premise_type(self, premise_type=None, ignore_parent=False):
        return (self.published_premises(ignore_parent=ignore_parent)
                .filter(premise_type=premise_type))

    because = curry(children_by_premise_type,
                    premise_type=SUPPORT, ignore_parent=True)
    but = curry(children_by_premise_type,
                premise_type=OBJECTION, ignore_parent=True)
    however = curry(children_by_premise_type,
                    premise_type=SITUATION, ignore_parent=True)

    def update_sibling_counts(self):
        for premise in self.premises.filter():
            premise.update_sibling_counts()

    def last_user(self):
        try:
            # add date_creation
            premise = self.premises.order_by("-pk")[0]
        except IndexError:
            user = self.user
        else:
            user = premise.user
        return user

    def width(self):
        return self.published_children(ignore_parent=True).count()

    def get_actor(self):
        """
        Encapsulated for newsfeed app.
        """
        return self.user

    def get_newsfeed_type(self):
        return NEWS_TYPE_CONTENTION

    def get_newsfeed_bundle(self):
        return {
            "title": self.title,
            "owner": self.owner,
            "uri": self.get_absolute_url()
        }

    def contributors(self):
        from profiles.models import Profile
        # avoid circular import

        return Profile.objects.filter(
            id__in=self.premises.values_list("user_id", flat=True)
        )


class Premise(DeletePreventionMixin, models.Model):
    argument = models.ForeignKey(Contention, related_name="premises")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_premises')
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

    def serialize(self, premise_lookup, authenticated_user=None):
        supported = False
        if authenticated_user is not None:
            supported = self.supporters.filter(
                id=authenticated_user.id
            ).exists()
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
            'supported_by_authenticated_user': supported,
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
            'fallacies': self.fallacies(authenticated_user),
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

    def sub_tree_ids(self, current=None, children_ids=None):
        # RETURNS ALL THE CHILD PREMISE IDS
        current = self if current is None else current
        children_ids = children_ids if children_ids != None else []
        for child in current.children.all():
            children_ids.append(child.id)
            self.sub_tree_ids(current=child, children_ids=children_ids)
        return children_ids

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

    def fallacies(self, authenticed_user=None):
        reports = self.reports.values('fallacy_type', 'reporter_id')
        fallacies = set(report['fallacy_type'] for report in reports)
        mapping = dict(FALLACY_TYPES)
        
        user_reports = set()
        if authenticed_user is not None:
            for report in reports:
                if report['reporter_id'] == authenticed_user.id:
                    user_reports.add(report['fallacy_type'])

        return [{
            'type': fallacy,
            'label': mapping.get(fallacy),
            'reported_by_authenticated_user': fallacy in user_reports
        } for fallacy in fallacies if fallacy]

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


class Comment(models.Model):
    premise = models.ForeignKey(Premise)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return smart_unicode(self.text)


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
