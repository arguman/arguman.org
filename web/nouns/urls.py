from django.conf.urls import patterns, url
from nouns.views import NounDetail, RelationCreate, ChannelDetail

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', NounDetail.as_view(), name="nouns_detail"),
    url(r'^(?P<slug>[-\w]+)/new-relation$', RelationCreate.as_view(), name="new_relation"),
)
