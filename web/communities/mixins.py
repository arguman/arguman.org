from communities.models import Community


class CommunityMixin(object):

    def get_community(self, subdomain):
        try:
            community = Community.objects.get(name=subdomain)
        except Community.DoesNotExist:
            community = None

        return community

    def apply_community_filter(self, queryset):
        community = self.request.community

        if community:
            return queryset.filter(community=community)

        return queryset
