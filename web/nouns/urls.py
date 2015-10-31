from django.conf.urls import patterns, url
from nouns.views import NounDetail

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', NounDetail.as_view(), name="nouns_detail"),
)
