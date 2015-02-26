from django.conf.urls import patterns, url
from .views import notification_list, notification_detail

urlpatterns = patterns(
    '',
    url(r'^$', notification_list,
        name='api-notification-list'),
    url(r'^(?P<pk>[0-9]+)/$', notification_detail,
        name='api-notification-detail'),
)
