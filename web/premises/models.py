# -*- coding: utf-8 -*-
from unidecode import unidecode

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode
from django.utils.functional import curry

from premises.managers import ContentionManager

OBJECTION = 0
SUPPORT = 1
SITUATION = 2

PREMISE_TYPES = (
    (OBJECTION, u"İtiraz"),
    (SUPPORT, u"Destek"),
    (SITUATION, u"Bilgilendirme"),
)


class Contention(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
    owner = models.CharField(max_length=255, null=True, blank=True)
    sources = models.TextField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    objects = ContentionManager()

    class Meta:
        ordering = ["-date_creation"]

    def __unicode__(self):
        return smart_unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'contention_detail', [self.slug]

    def save(self, *args, **kwargs):
        """
        - Make unique slug if it is not given.
        """
        if not self.slug:
            slug = slugify(unidecode(self.title))
            duplications = Contention.objects.filter(slug=slug).count()
            if duplications > 0:
                self.slug = "%s-%s" % (slug, duplications + 1)
            else:
                self.slug = slug
        return super(Contention, self).save(*args, **kwargs)

    def published_premises(self):
        return self.premises.filter(is_approved=True, parent=None)

    def children_by_premise_type(self, premise_type=None):
        return self.published_premises().filter(premise_type=premise_type)

    because = curry(children_by_premise_type, premise_type=SUPPORT)
    but = curry(children_by_premise_type, premise_type=OBJECTION)
    however = curry(children_by_premise_type, premise_type=SITUATION)


class Premise(models.Model):
    argument = models.ForeignKey(Contention, related_name="premises")
    user = models.ForeignKey(User)
    parent = models.ForeignKey("self", related_name="children",
                               null=True, blank=True)
    premise_type = models.IntegerField(choices=PREMISE_TYPES)
    text = models.TextField(null=True, blank=True)
    sources = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __unicode__(self):
        return smart_unicode(self.text)

    def published_children(self):
        return self.children.filter(is_approved=True)


class Comment(models.Model):
    premise = models.ForeignKey(Premise)
    user = models.ForeignKey(User)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return smart_unicode(self.text)
