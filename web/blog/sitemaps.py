from django.contrib.sitemaps import Sitemap

from blog.models import Post


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return Post.published_objects.all()

    def lastmod(self, obj):
        return obj.date_modified
