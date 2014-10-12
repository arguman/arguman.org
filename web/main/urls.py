from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('premises.urls')),
    url(r'^', include('profiles.urls')),
    url(r'^', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
