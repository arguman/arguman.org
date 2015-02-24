from django.conf.urls import patterns, url
from .views import public_newsfeed, private_newsfeed


urlpatterns = patterns(
    '',
    url(r'^public/$', public_newsfeed, name='api-public-newfeed'),
    url(r'^private/$', private_newsfeed, name='api-private-newfeed'),
)
