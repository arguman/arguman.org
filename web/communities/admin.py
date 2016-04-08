from django.contrib import admin

from communities.models import Community, Membership


class CommunityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Community, CommunityAdmin)


class MembershipAdmin(admin.ModelAdmin):
    pass
admin.site.register(Membership, MembershipAdmin)
