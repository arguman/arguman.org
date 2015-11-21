from django.contrib import admin

from communities.models import Community


class CommunityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Community, CommunityAdmin)
