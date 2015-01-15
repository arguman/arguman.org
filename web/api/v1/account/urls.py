from django.conf.urls import patterns, url
from .views import profile_detail


urlpatterns = patterns(
    '',
    url(r'^(?P<username>[A-Za-z0-9-_]+)/$', profile_detail,
        name='api-profile-detail'),
)
