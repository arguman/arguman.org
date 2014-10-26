# -*- coding: utf-8 -*-
from uuid import uuid4
from django.core import validators
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from unidecode import unidecode

from django.conf import settings
from django.template.loader import render_to_string
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode
from django.utils.functional import curry
from premises.constants import MAX_PREMISE_CONTENT_LENGTH

from premises.managers import ContentionManager

OBJECTION = 0
SUPPORT = 1
SITUATION = 2

PREMISE_TYPES = (
    (OBJECTION, u"ama"),
    (SUPPORT, u"çünkü"),
    (SITUATION, u"ancak"),
)


class Contention(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Argüman",
        help_text=render_to_string("premises/examples/contention.html"))
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(
        null=True, blank=True, verbose_name="Ek bilgiler",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    owner = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="Orijinal söylem",
        help_text=render_to_string("premises/examples/owner.html"))
    sources = models.TextField(
        null=True, blank=True,
        verbose_name="Kaynaklar",
        help_text=render_to_string("premises/examples/sources.html"))
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True,
                                             auto_now=True)

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


class Premise(models.Model):
    argument = models.ForeignKey(Contention, related_name="premises")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    parent = models.ForeignKey("self", related_name="children",
                               null=True, blank=True,
                               verbose_name="Öncülü",
                               help_text="Önermenin öncülü. Eğer boş bırakılırsa"
                                         "ana argümanın bir önermesi olur.")
    premise_type = models.IntegerField(
        default=SUPPORT,
        choices=PREMISE_TYPES, verbose_name="Önerme Tipi",
        help_text=render_to_string("premises/examples/premise_type.html"))
    text = models.TextField(
        null=True, blank=True,
        verbose_name="Önermenin İçeriği",
        help_text=render_to_string("premises/examples/premise.html"),
        validators=[validators.MaxLengthValidator(MAX_PREMISE_CONTENT_LENGTH)])
    sources = models.TextField(
        null=True, blank=True, verbose_name="Kaynaklar",
        help_text=render_to_string("premises/examples/premise_source.html"))
    is_approved = models.BooleanField(default=False, verbose_name="Yayınla")

    # denormalized fields
    sibling_count = models.IntegerField(default=1)
    like_count = models.PositiveIntegerField(default=0, db_index=True, editable=False)
    unlike_count = models.PositiveIntegerField(default=0, db_index=True, editable=False)

    def __unicode__(self):
        return smart_unicode(self.text)

    @models.permalink
    def get_absolute_url(self):
        return 'contention_detail', [self.argument.slug]

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


class Comment(models.Model):
    premise = models.ForeignKey(Premise)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return smart_unicode(self.text)


class Vote(models.Model):
    premise = models.ForeignKey(Premise)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    like = models.BooleanField(default=False, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return smart_unicode(self.premise)

    class Meta:
        ordering = ("date_created",)
        unique_together = ("premise", "user")


@receiver(post_save, sender=Vote)
@receiver(post_delete, sender=Vote)
def update_premises_like_and_unlike_count(sender, instance, **kwargs):
    premises_like_count = Vote.objects.filter(premise_id=instance.premise_id, like=True).count()
    premises_unlike_count = Vote.objects.filter(premise_id=instance.premise_id, like=False).count()
    Premise.objects.filter(id=instance.premise_id).update(like_count=premises_like_count,
                                                          unlike_count=premises_unlike_count)