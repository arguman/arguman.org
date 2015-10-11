from django.contrib.sitemaps import Sitemap

from profiles.models import Profile


class ProfileSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return Profile.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
