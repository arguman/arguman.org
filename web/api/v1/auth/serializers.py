from rest_framework import serializers

from profiles.models import Profile


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
