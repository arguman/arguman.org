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


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password',)

    def validate_username(self, value):
        try:
            Profile._default_manager.get(username__iexact=value)
        except Profile.DoesNotExist:
            return value
        raise serializers.ValidationError('username already exists')

    def create(self, validated_data):
        user = Profile(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # FIXME
        self.fields.pop('password')
        return user
