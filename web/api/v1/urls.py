from django.conf.urls import patterns, include, url
from api.v1.users.views import profile_me


urlpatterns = patterns(
    '',
    url(r'^auth/', include('api.v1.auth.urls')),
    url(r'^user/$', profile_me, name='api-me'),
    url(r'^users/', include('api.v1.users.urls')),
    url(r'^arguments/', include('api.v1.arguments.urls')),
    url(r'^newsfeed/', include('api.v1.newsfeed.urls')),
)
