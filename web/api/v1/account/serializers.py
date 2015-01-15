from django.core.urlresolvers import reverse
from rest_framework import serializers
from profiles.models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'absolute_url',)

    def get_absolute_url(self, obj):
        return reverse("api-profile-detail", args=[obj.username])
