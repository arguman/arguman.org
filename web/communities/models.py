from django.conf import settings
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


COMMUNITY_TYPES = (
    ('public', _('Public')),
    ('restricted', _('Restricted')),
    ('private', _('Private')),
)


class Community(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    community_type = models.CharField(max_length=255,
                                      choices=COMMUNITY_TYPES)
    language = models.CharField(max_length=255)
    about = models.TextField(blank=True, null=True)
    terms_of_service = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Communities"

    def __unicode__(self):
        return smart_unicode(self.name)


class Membership(models.Model):
    community = models.ForeignKey(Community)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="memberships")
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    can_create_argument = models.BooleanField(default=False)
    can_create_premise = models.BooleanField(default=False)

    def __unicode__(self):
        return smart_unicode(self.user.username)
