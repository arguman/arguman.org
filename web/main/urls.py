from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('newsfeed.urls')),
    url(r'^', include('premises.urls')),
    url(r'^', include('profiles.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
