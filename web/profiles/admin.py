from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django_gravatar.templatetags.gravatar import gravatar
from profiles.models import Profile


class ProfileAdmin(UserAdmin):

    list_display = ('gravatar', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    ordering = ("-id", )

    def gravatar(self, obj):
        return '<img src="%s" />' % gravatar(obj)
    gravatar.allow_tags = True

admin.site.register(Profile, ProfileAdmin)
