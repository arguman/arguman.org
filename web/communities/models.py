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

    def is_restricted(self):
        return self.community_type == 'restricted'

    def is_private(self):
        return self.community_type == 'private'

    def is_public(self):
        return self.community_type == 'public'

    def get_membership(self, user):
        if user.is_anonymous():
            return

        try:
            return self.memberships.get(user=user)
        except Membership.DoesNotExist:
            return

    def is_member(self, user):
        return bool(self.get_membership(user))

    def add_member(self, user):
        membership = self.get_membership(user)

        if membership:
            return membership

        return self.memberships.create(
            user=user,
            is_active=True,
            is_owner=False,
            can_create_argument=not self.is_restricted,
            can_create_premise=not self.is_restricted
        )

    def user_can_create_argument(self, user):
        membership = self.get_membership(user)

        if not membership:
            return False

        if self.is_restricted():
            return membership.can_create_argument

        return True

    def user_can_view(self, user):
        if self.is_private():
            return self.is_member(user)

        return True


class Membership(models.Model):
    community = models.ForeignKey(Community, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="memberships")
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    can_create_argument = models.BooleanField(default=False)
    can_create_premise = models.BooleanField(default=False)

    def __unicode__(self):
        return smart_unicode(self.user.username)
