from django.conf.urls import patterns, url

from premises.views import (ContentionDetailView, HomeView,
                            ArgumentCreationView, PremiseCreationView,
                            PremiseDeleteView)


urlpatterns = patterns('',
   url(r'^$', HomeView.as_view(), name='home'),
   url(r'^new-argument$',
       ArgumentCreationView.as_view(),
       name='new_argument'),
   url(r'^(?P<slug>[\w-]+)$',
        ContentionDetailView.as_view(),
        name='contention_detail'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/delete',
        PremiseDeleteView.as_view(),
        name='delete_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/(?P<pk>[0-9]+)/insert',
        PremiseCreationView.as_view(),
        name='insert_premise'),
   url(r'^(?P<slug>[\w-]+)/premises/new',
        PremiseCreationView.as_view(),
        name='new_premise'),

)
