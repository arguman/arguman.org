# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters, status
from rest_framework.response import Response

from profiles.models import Notification
from .serializers import NotificationSerializer


class NotificationViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 20
    serializer_class = NotificationSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('is_read',)
    ordering_fields = ('date_created',)

    def get_queryset(self):
        user = self.request.user
        return user.notifications.select_related('sender', 'recipient')

    def mark_as_read_all_notification(self, request):
        user = self.request.user
        user.notifications.filter(is_read=False).update(is_read=True)
        return Response(status=status.HTTP_200_OK)

    def mark_as_read_single_notification(self, request, pk=None):
        notification = self.get_object()
        notification.is_read=True
        notification.save()
        return Response(status=status.HTTP_200_OK)


notification_list = NotificationViewset.as_view(
    {'get': 'list', 'patch': 'mark_as_read_all_notification'}
)

notification_detail = NotificationViewset.as_view(
    {'get': 'retrieve', 'patch': 'mark_as_read_single_notification'}
)
