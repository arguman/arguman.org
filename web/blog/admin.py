from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_published"]
    list_filter = ["is_published"]
    search_fields = ["title", "slug", "content"]
    actions = ["publish", "mark_as_draft"]
    prepopulated_fields = {
        "slug": ("title", )
    }

    def publish(self, request, qs):
        qs.update(is_published=True)
    publish.short_description = _("Publish selected posts")

    def mark_as_draft(self, request, qs):
        qs.update(is_published=False)
    mark_as_draft.short_description = _("Mark as draft selected posts")


admin.site.register(Post, PostAdmin)
