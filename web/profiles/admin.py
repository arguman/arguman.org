from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django_gravatar.templatetags.gravatar import gravatar as gravatar_for_user

from profiles.models import Profile, Notification


class ProfileAdmin(UserAdmin):

    list_display = ('gravatar', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    ordering = ("-id", )

    def gravatar(self, obj):
        return gravatar_for_user(obj)
    gravatar.allow_tags = True


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'notification_type')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
