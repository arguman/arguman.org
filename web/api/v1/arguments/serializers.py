from django.core.urlresolvers import reverse

from rest_framework import serializers

from premises.models import (
    Contention, Premise, Report, get_fallacy_types, PREMISE_TYPES)
from premises.signals import reported_as_fallacy
from api.v1.users.serializers import UserProfileSerializer


class PremisesSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    premise_type = serializers.ReadOnlyField(source='get_premise_type_display')
    supporters = UserProfileSerializer(many=True, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Premise.objects.all(), required=False)
    text = serializers.CharField(required=True, max_length=300)
    premise_type = serializers.ChoiceField(
        required=True, choices=PREMISE_TYPES)

    class Meta:
        model = Premise
        fields = ('id', 'user', 'text', 'sources', 'parent',
                  'absolute_url', 'premise_type',
                  'date_creation', 'supporters',)
        read_only_fields = ('id', 'absolute_url', 'date_creation')

    def create(self, validated_data):
        instance = Premise(**validated_data)
        instance.user = self.initial['user']
        instance.ip_address = self.initial['ip']
        instance.argument = self.initial['argument']
        instance.is_approved = True
        instance.save()
        return instance

    def get_absolute_url(self, obj):
        return reverse("api-premise-detail", args=[obj.argument.id, obj.id])


class ContentionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    premises = PremisesSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    report_count = serializers.ReadOnlyField(source='reports.count')
    is_published = serializers.BooleanField(required=True)

    class Meta:
        model = Contention
        fields = ('id', 'user', 'title', 'slug', 'description',
                  'owner', 'sources', 'premises', 'date_creation',
                  'absolute_url', 'report_count',
                  'is_featured', 'is_published',)
        read_only_fields = ('id', 'slug', 'absolute_url',
                            'is_featured', 'date_creation')

    def create(self, validated_data):
        instance = Contention(**validated_data)
        instance.user = self.initial['user']
        instance.ip_address = self.initial['ip']
        instance.save()
        return instance

    def get_absolute_url(self, obj):
        return reverse("api-contention-detail", args=[obj.id])


class PremiseReportSerializer(serializers.ModelSerializer):
    reporter = UserProfileSerializer(read_only=True)
    premise = PremisesSerializer(read_only=True)
    contention = ContentionSerializer(read_only=True)
    fallacy_type = serializers.ChoiceField(
        required=True, choices=get_fallacy_types())

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
