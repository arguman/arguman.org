from django.conf.urls import patterns, url
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegisterView


urlpatterns = patterns(
    '',
    url(r'^login/$', obtain_auth_token, name="api-login"),
    url(r'^register/$', UserRegisterView.as_view(), name="api-register"),
)
