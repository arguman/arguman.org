from django.conf.urls import patterns, url

from premises.views import (ContentionDetailView, HomeView,
                            ArgumentCreationView, PremiseCreationView)


urlpatterns = patterns('',
   url(r'^$', HomeView.as_view(), name='home'),
   url(r'^new-argument$', ArgumentCreationView.as_view(), name='new_argument'),
    url(r'^(?P<slug>[\w-]+)$', ContentionDetailView.as_view(),
        name='contention_detail'),
    url(r'^(?P<slug>[\w-]+)$/new-premise', PremiseCreationView.as_view(),
        name='contention_detail'),
)
