from django.core.urlresolvers import reverse

from rest_framework import serializers

from premises.models import Contention, Premise
from api.v1.account.serializers import UserProfileSerializer


class PremisesSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Premise
        fields = ('id', 'user', 'text', 'sources', 'parent',)


class ContentionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    premises = PremisesSerializer(many=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Contention
        fields = ('id', 'user', 'title', 'slug', 'description',
                  'owner', 'sources', 'premises', 'absolute_url',)

    def get_absolute_url(self, obj):
        return reverse("api-contention-detail", args=[obj.id])
