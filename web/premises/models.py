# -*- coding: utf-8 -*-
from uuid import uuid4
from markdown2 import markdown
from unidecode import unidecode

from django.utils.html import escape
from django.core import validators
from django.conf import settings
from django.template.loader import render_to_string
from django.db import models
from django.db.models import Count, Q
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from newsfeed.constants import (
    NEWS_TYPE_FALLACY, NEWS_TYPE_PREMISE, NEWS_TYPE_CONTENTION)
from premises.constants import MAX_PREMISE_CONTENT_LENGTH
from premises.managers import ContentionManager, DeletePreventionManager
from premises.mixins import DeletePreventionMixin
from premises.utils import replace_with_link
from nouns.models import Noun
from nouns.utils import tokenize

OBJECTION = 0
SUPPORT = 1
SITUATION = 2

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
    date_modification = models.DateTimeField(auto_now_add=True,
                                             auto_now=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=5, null=True,
                                choices=[(language, language) for language in
                                        settings.AVAILABLE_LANGUAGES])
    nouns = models.ManyToManyField('nouns.Noun', related_name="contentions",
                                   blank=True, null=True)

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

        instance = super(Contention, self).save(*args, **kwargs)
        self.save_nouns()
        return instance

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

    def extract_nouns(self):
        tokens = ' '.join(tokenize(self.title))

        nouns = (Noun
                 .objects
                 .prefetch_related('synonyms')
                 .filter(is_active=True))

        for noun in nouns:
            if noun.text in tokens:
                yield noun
                continue
            for synonym in noun.synonyms.all():
                if synonym.text in tokens:
                    yield noun
                    continue

    def save_nouns(self):
        nouns = self.extract_nouns()
        for noun in nouns:
            self.nouns.add(noun)

    def formatted_title(self, tag='a'):
        title = strip_tags(self.title)
        select = {'length': 'Length(nouns_noun.text)'}
        nouns = (self
                 .nouns
                 .extra(select=select)
                 .prefetch_related('synonyms')
                 .order_by('-length'))

        for noun in nouns:
            synonyms = (
                noun.synonyms.values_list(
                    'text', flat=True
                )
            )
            sorted_synonyms = sorted(
                synonyms,
                key=len,
                reverse=True
            )

            for synonym in sorted_synonyms:
                replaced = replace_with_link(
                    title,
                    synonym,
                    noun.get_absolute_url(),
                    tag
                )

                if replaced is not None:
                    title = replaced
                    continue

            replaced = replace_with_link(
                title,
                noun.text,
                noun.get_absolute_url(),
                tag
            )

            if replaced is not None:
                title = replaced

        return title

    highlighted_title = curry(formatted_title, tag='span')


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
