from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^auth/', include('api.v1.auth.urls', namespace='api-auth')),
)
