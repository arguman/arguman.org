from django.core.urlresolvers import reverse

from rest_framework import serializers

from premises.models import Contention, Premise, Report
from api.v1.account.serializers import UserProfileSerializer


class PremisesSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Premise
        fields = ('id', 'user', 'text', 'sources', 'parent', 'absolute_url',)

    def get_absolute_url(self, obj):
        return reverse("api-premise-detail", args=[obj.argument.id, obj.id])


class ContentionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    premises = PremisesSerializer(many=True)
    absolute_url = serializers.SerializerMethodField()
    report_count = serializers.ReadOnlyField(source='reports.count')

    class Meta:
        model = Contention
        fields = ('id', 'user', 'title', 'slug', 'description',
                  'owner', 'sources', 'premises',
                  'absolute_url', 'report_count')

    def get_absolute_url(self, obj):
        return reverse("api-contention-detail", args=[obj.id])


class PremiseReportSerializer(serializers.ModelSerializer):
    reporter = UserProfileSerializer(read_only=True)
    premise = PremisesSerializer(read_only=True)
    contention = ContentionSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('fallacy_type', 'reporter', 'premise', 'contention',)


    def create(self, validated_data):
        instance = Report(**validated_data)
        instance.reporter = self.initial['reporter']
        instance.premise = self.initial['premise']
        instance.contention = self.initial['contention']
        instance.save()
        return instance
