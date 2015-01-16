from django.conf.urls import patterns, url
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns(
    '',
    url(r'^token/$', obtain_auth_token, name="generate-token"),
)
