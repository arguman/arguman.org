from django.contrib.sitemaps import Sitemap

from premises.models import Contention


class ArgumentSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return Contention.objects.language().filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date_modification
