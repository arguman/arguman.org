# -*- coding: utf-8 -*-
from django.utils.html import strip_tags

from rest_framework import serializers

from profiles.models import Notification
from api.v1.users.serializers import UserProfileSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer()
    recipient = UserProfileSerializer()
    notification_type = serializers.ReadOnlyField(
        source='get_notification_type_display')
    text = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('sender', 'recipient', 'date_created', 'notification_type',
                  'is_read', 'target_object_id', 'id', 'text',)

    def get_text(self, obj):
        return strip_tags(obj.render()).strip().replace('\n', ' ')
