from django.conf.urls import patterns, url
from .views import (contention_list, contention_detail, premise_detail,
                    premises_list, premise_report, premise_support,
                    premise_supporters)


urlpatterns = patterns(
    '',
    url(r'^$', contention_list,
        name='api-contention-list'),
    url(r'^(?P<pk>[0-9]+)/$', contention_detail,
        name='api-contention-detail'),
    url(r'^(?P<pk>[0-9]+)/premises/$', premises_list,
        name='api-contention-premises'),
    url(r'^(?P<pk>[0-9]+)/premises/(?P<premise_id>[0-9]+)/$',
        premise_detail, name='api-premise-detail'),
    url(r'^(?P<pk>[0-9]+)/premises/(?P<premise_id>[0-9]+)/report/$',
        premise_report, name='api-premise-detail'),
    url(r'^(?P<pk>[0-9]+)/premises/(?P<premise_id>[0-9]+)/support/$',
        premise_support, name='api-premise-detail'),
    url(r'^(?P<pk>[0-9]+)/premises/(?P<premise_id>[0-9]+)/supporters/$',
        premise_supporters, name='api-premise-supporters'),
)
