from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.templatetags.static import static
from django.views.decorators.cache import cache_page

from blog.sitemaps import BlogSitemap
from nouns.views import ChannelDetail
from profiles.sitemaps import ProfileSitemap
from premises.sitemaps import ArgumentSitemap, PremiseSitemap

admin.autodiscover()

sitemaps = {
    'blog': BlogSitemap(),
    'user': ProfileSitemap(),
    'argument': ArgumentSitemap(),
    'premise': PremiseSitemap()
}

urlpatterns = patterns('',
    url(r'^', include('newsfeed.urls')),
    url(r'^', include('premises.urls')),
    url(r'^', include('profiles.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^nouns/', include('nouns.urls')),
    url(r'^communities/', include('communities.urls')),
    url(r'^channels/(?P<slug>[-\w]+)$',
        ChannelDetail.as_view(), name="channel_detail"),
    url(r'^', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),

    # Sitemap
    url(r'^sitemap\.xml$',
        cache_page(86400)(sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
)
