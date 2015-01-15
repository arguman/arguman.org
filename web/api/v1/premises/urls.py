from django.conf.urls import patterns, url
from .views import contention_list, contention_detail, premises_list


urlpatterns = patterns(
    '',
    url(r'^$', contention_list,
        name='api-contention-list'),
    url(r'^(?P<pk>[0-9]+)/$', contention_detail,
        name='api-contention-detail'),
    url(r'^(?P<pk>[0-9]+)/premises/$', premises_list,
        name='api-contention-premises'),
)
