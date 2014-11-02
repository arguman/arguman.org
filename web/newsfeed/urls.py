from django.conf.urls import patterns, url

from newsfeed.views import NewsfeedView


urlpatterns = patterns('',
   url(r'^newsfeed$', NewsfeedView.as_view(), name='newsfeed'),
)
