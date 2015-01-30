from django.core.urlresolvers import reverse

from rest_framework import serializers

from premises.models import Contention, Premise, Report
from premises.signals import reported_as_fallacy
from api.v1.account.serializers import UserProfileSerializer


class PremisesSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    absolute_url = serializers.SerializerMethodField()
    premise_type = serializers.ReadOnlyField(source='get_premise_type_display')
    supporters = UserProfileSerializer(many=True)

    class Meta:
        model = Premise
        fields = ('id', 'user', 'text', 'sources', 'parent',
                  'absolute_url', 'premise_type',
                  'date_creation', 'supporters',)

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
                  'owner', 'sources', 'premises', 'date_creation',
                  'absolute_url', 'report_count', 'is_featured')

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
        reported_as_fallacy.send(sender=self, report=instance)
        return instance
