from django.core.urlresolvers import reverse

from rest_framework import serializers
from django_gravatar.templatetags import gravatar

from profiles.models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = ('id', 'username', 'absolute_url', 'avatar',)

    def get_absolute_url(self, obj):
        return reverse("api-profile-detail", args=[obj.username])

    def get_avatar(self, obj):
        return gravatar.get_gravatar_url(obj.email)
