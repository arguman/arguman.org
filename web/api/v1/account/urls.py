from django.conf.urls import patterns, url
from .views import profile_detail, UserRegisterView


urlpatterns = patterns(
    '',
    url(r'^$', UserRegisterView.as_view(),
        name='api-user-register'),
    url(r'^(?P<username>[A-Za-z0-9-_]+)/$', profile_detail,
        name='api-profile-detail'),
)
