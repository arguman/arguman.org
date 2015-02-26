from rest_framework import serializers

from profiles.models import Notification
from api.v1.users.serializers import UserProfileSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer()
    recipient = UserProfileSerializer()
    notification_type = serializers.ReadOnlyField(
        source='get_notification_type_display')
    target_object_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('sender', 'recipient', 'date_created', 'notification_type',
                  'is_read', 'target_object_id', 'id',)

    def target_object_type(self, obj):
        return obj.get_target_type().__name__
