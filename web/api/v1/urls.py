from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^auth/', include('api.v1.auth.urls')),
    url(r'^account/', include('api.v1.account.urls')),
    url(r'^premises/', include('api.v1.premises.urls')),
)
