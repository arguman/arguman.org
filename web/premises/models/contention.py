from uuid import uuid4
from unidecode import unidecode
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.encoding import smart_unicode
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from ..mixins import DeletePreventionMixin
from ..managers import ContentionManager
from newsfeed import NEWS_TYPE_CONTENTION
from . import Channel, OBJECTION, SUPPORT, SITUATION


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
    language = models.CharField(max_length=5, null=True)

    objects = ContentionManager()

    class Meta:
        ordering = ["-date_creation"]

    def __unicode__(self):
        return smart_unicode(self.title)

    def serialize(self):
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
            'premises': [premise.serialize(premises)
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
